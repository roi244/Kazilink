from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import MissionOrder

from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, mission_id):
    mission = get_object_or_404(MissionOrder, id=mission_id, client=request.user)
    if mission.status != MissionOrder.STATUS_COMPLETED:
        messages.error(request, 'Vous pouvez noter uniquement une mission terminee.')
        return redirect('orders:my_orders')

    if hasattr(mission, 'review'):
        messages.info(request, 'Un avis existe deja pour cette mission.')
        return redirect('orders:my_orders')

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.mission = mission
        review.client = request.user
        review.provider = mission.provider_service.provider
        review.save()
        messages.success(request, 'Avis publie.')
        return redirect('orders:my_orders')

    return render(request, 'reviews/add_review.html', {'form': form, 'mission': mission})


def provider_reviews(request, provider_id):
    reviews = Review.objects.filter(provider_id=provider_id).select_related('client', 'mission')
    return render(request, 'reviews/provider_reviews.html', {'reviews': reviews})
