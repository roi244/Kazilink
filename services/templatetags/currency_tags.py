from decimal import Decimal, ROUND_HALF_UP

from django import template

from services.currency import get_currency_rates, get_supported_currencies

register = template.Library()


@register.simple_tag(takes_context=True)
def money(context, amount):
    request = context.get('request')
    supported = get_supported_currencies()
    rates = get_currency_rates()

    selected_currency = 'FCFA'
    if request is not None:
        selected_currency = request.session.get('currency', 'FCFA').upper()

    if selected_currency not in supported:
        selected_currency = 'FCFA'

    value_fcfa = Decimal(str(amount or 0))

    if selected_currency == 'FCFA':
        fcfa_value = value_fcfa.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return f"{fcfa_value:,.0f} FCFA".replace(',', ' ')

    rate = rates.get(selected_currency)
    if not rate or rate <= 0:
        rate = rates.get('FCFA', Decimal('1'))

    converted = (value_fcfa / rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return f"{converted:,.2f} {selected_currency}".replace(',', ' ')
