from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import UserProfile
from services.models import ProviderService

from .forms import ManualPaymentProofForm, MissionRequestForm
from .models import MissionOrder

try:
    import stripe
except ImportError:
    stripe = None


def _get_stripe_client():
    if stripe is None or not settings.STRIPE_SECRET_KEY:
        return None
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def _stripe_ready():
    return bool(settings.STRIPE_SECRET_KEY and settings.STRIPE_WEBHOOK_SECRET)


@login_required
def create_order(request, service_id):
    profile = request.user.profile
    if profile.role != UserProfile.ROLE_CLIENT:
        messages.error(request, 'Seuls les clients peuvent demander une mission.')
        return redirect('services:home')

    provider_service = get_object_or_404(ProviderService, id=service_id, is_active=True)
    form = MissionRequestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.client = request.user
        order.provider_service = provider_service
        order.payment_provider = 'stripe' if _stripe_ready() else 'manual'
        order.save()
        messages.success(request, 'Mission creee. Validez maintenant le paiement pour confirmer la demande.')
        return redirect('orders:my_orders')

    return render(
        request,
        'orders/create_order.html',
        {
            'form': form,
            'provider_service': provider_service,
        },
    )


@login_required
def my_orders(request):
    profile = request.user.profile
    if profile.role == UserProfile.ROLE_PROVIDER:
        orders = MissionOrder.objects.filter(provider_service__provider=request.user).select_related(
            'client', 'provider_service', 'provider_service__category'
        )
    else:
        orders = MissionOrder.objects.filter(client=request.user).select_related(
            'provider_service', 'provider_service__provider', 'provider_service__category'
        )

    orders = list(orders)
    for order in orders:
        order.has_review = hasattr(order, 'review')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders,
            'stripe_ready': _stripe_ready(),
            'manual_payment_enabled': settings.MANUAL_PAYMENT_ENABLED,
        },
    )


@login_required
def start_checkout(request, order_id):
    order = get_object_or_404(MissionOrder, id=order_id, client=request.user)

    if order.is_paid:
        messages.info(request, 'Cette mission est deja payee.')
        return redirect('orders:my_orders')

    stripe_client = _get_stripe_client()
    if stripe_client is None:
        messages.error(
            request,
            "Paiement en ligne indisponible. Utilisez le paiement manuel.",
        )
        return redirect('orders:manual_payment', order_id=order.id)

    success_url = request.build_absolute_uri(reverse('orders:payment_success', args=[order.id]))
    cancel_url = request.build_absolute_uri(reverse('orders:payment_cancel', args=[order.id]))

    checkout_kwargs = {
        'mode': 'payment',
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': [
            {
                'price_data': {
                    'currency': 'xof',
                    'product_data': {
                        'name': f"Mission #{order.id} - {order.provider_service.title}",
                        'description': f"Prestataire {order.provider_service.provider.username} a {order.city}",
                    },
                    'unit_amount': int(order.total_amount),
                },
                'quantity': 1,
            }
        ],
        'metadata': {'order_id': str(order.id)},
        'payment_intent_data': {'metadata': {'order_id': str(order.id)}},
    }
    if request.user.email:
        checkout_kwargs['customer_email'] = request.user.email

    session = stripe_client.checkout.Session.create(**checkout_kwargs)

    order.payment_status = MissionOrder.PAYMENT_REQUIRES_ACTION
    order.payment_provider = 'stripe'
    order.payment_reference = session.get('id', '')
    order.save(update_fields=['payment_status', 'payment_provider', 'payment_reference', 'commission_amount'])

    return redirect(session.url, permanent=False)


@login_required
def manual_payment(request, order_id):
    if not settings.MANUAL_PAYMENT_ENABLED:
        messages.error(request, 'Le paiement manuel est desactive.')
        return redirect('orders:my_orders')

    order = get_object_or_404(MissionOrder, id=order_id, client=request.user)
    form = ManualPaymentProofForm(request.POST or None, initial={'payment_reference': order.payment_reference})

    if request.method == 'POST' and form.is_valid():
        order.payment_provider = 'manual'
        order.payment_reference = form.cleaned_data['payment_reference']
        order.payment_status = MissionOrder.PAYMENT_REQUIRES_ACTION
        order.save(update_fields=['payment_provider', 'payment_reference', 'payment_status', 'commission_amount'])
        messages.success(request, 'Preuve envoyee. Le prestataire peut maintenant valider le paiement.')
        return redirect('orders:my_orders')

    context = {
        'order': order,
        'form': form,
        'payment_label': settings.MANUAL_PAYMENT_LABEL,
        'payment_number': settings.MANUAL_PAYMENT_NUMBER,
        'payment_holder': settings.MANUAL_PAYMENT_HOLDER,
        'payment_note': settings.MANUAL_PAYMENT_NOTE,
    }
    return render(request, 'orders/manual_payment.html', context)


@login_required
def confirm_manual_payment(request, order_id):
    order = get_object_or_404(MissionOrder, id=order_id)
    is_provider_owner = order.provider_service.provider_id == request.user.id

    if not is_provider_owner and not request.user.is_staff:
        messages.error(request, 'Action non autorisee.')
        return redirect('orders:my_orders')

    if order.payment_status == MissionOrder.PAYMENT_PAID:
        messages.info(request, 'Paiement deja valide.')
        return redirect('orders:my_orders')

    if not order.payment_reference:
        messages.error(request, 'Aucune reference de paiement fournie par le client.')
        return redirect('orders:my_orders')

    order.mark_paid(payment_reference=order.payment_reference, amount=order.total_amount)
    order.save(update_fields=['payment_status', 'payment_reference', 'amount_paid', 'paid_at', 'commission_amount'])
    messages.success(request, 'Paiement valide. La mission peut etre acceptee.')
    return redirect('orders:my_orders')


@login_required
def payment_success(request, order_id):
    get_object_or_404(MissionOrder, id=order_id, client=request.user)
    messages.success(request, 'Retour de paiement recu. Confirmation en cours.')
    return redirect('orders:my_orders')


@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(MissionOrder, id=order_id, client=request.user)
    if order.payment_status == MissionOrder.PAYMENT_REQUIRES_ACTION and order.payment_provider == 'stripe':
        order.payment_status = MissionOrder.PAYMENT_UNPAID
        order.save(update_fields=['payment_status', 'commission_amount'])
    messages.warning(request, 'Paiement annule. Vous pouvez reessayer quand vous voulez.')
    return redirect('orders:my_orders')


@csrf_exempt
def stripe_webhook(request):
    stripe_client = _get_stripe_client()
    if stripe_client is None or not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=400)

    payload = request.body
    signature = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe_client.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        return HttpResponse(status=400)

    event_type = event.get('type')
    data = event.get('data', {}).get('object', {})

    if event_type == 'checkout.session.completed':
        order_id = (data.get('metadata') or {}).get('order_id')
        if order_id:
            order = MissionOrder.objects.filter(id=order_id).first()
            if order:
                amount_total = data.get('amount_total')
                amount_paid = Decimal(amount_total) / Decimal('100') if amount_total is not None else order.total_amount
                order.mark_paid(payment_reference=data.get('payment_intent') or data.get('id', ''), amount=amount_paid)
                order.save(update_fields=['payment_status', 'payment_reference', 'amount_paid', 'paid_at', 'commission_amount'])

    if event_type == 'checkout.session.expired':
        order_id = (data.get('metadata') or {}).get('order_id')
        if order_id:
            order = MissionOrder.objects.filter(id=order_id, payment_status=MissionOrder.PAYMENT_REQUIRES_ACTION).first()
            if order:
                order.payment_status = MissionOrder.PAYMENT_FAILED
                order.save(update_fields=['payment_status', 'commission_amount'])

    return HttpResponse(status=200)


@login_required
def update_status(request, order_id, status):
    order = get_object_or_404(MissionOrder, id=order_id)
    allowed_status = {
        MissionOrder.STATUS_ACCEPTED,
        MissionOrder.STATUS_COMPLETED,
        MissionOrder.STATUS_CANCELLED,
    }

    if status not in allowed_status:
        messages.error(request, 'Statut invalide.')
        return redirect('orders:my_orders')

    is_provider_owner = order.provider_service.provider_id == request.user.id
    is_client_owner = order.client_id == request.user.id

    if not (is_provider_owner or is_client_owner):
        messages.error(request, 'Action non autorisee.')
        return redirect('orders:my_orders')

    if status in {MissionOrder.STATUS_ACCEPTED, MissionOrder.STATUS_COMPLETED} and not order.is_paid:
        messages.error(request, 'Paiement non confirme: impossible de continuer la mission.')
        return redirect('orders:my_orders')

    order.status = status
    order.save(update_fields=['status', 'commission_amount'])
    messages.success(request, 'Statut mis a jour.')
    return redirect('orders:my_orders')
