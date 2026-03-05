from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django import template

register = template.Library()

SUPPORTED_CURRENCIES = ('FCFA', 'EUR')


@register.simple_tag(takes_context=True)
def money(context, amount):
    request = context.get('request')
    selected_currency = 'FCFA'

    if request is not None:
        selected_currency = request.session.get('currency', 'FCFA').upper()

    if selected_currency not in SUPPORTED_CURRENCIES:
        selected_currency = 'FCFA'

    value = Decimal(str(amount or 0))

    if selected_currency == 'EUR':
        rate = Decimal(str(getattr(settings, 'CURRENCY_RATE_EUR', '655.957')))
        converted = (value / rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"{converted:,.2f} EUR".replace(',', ' ')

    fcfa_value = value.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return f"{fcfa_value:,.0f} FCFA".replace(',', ' ')
