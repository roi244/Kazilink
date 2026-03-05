from django.conf import settings

SUPPORTED_CURRENCIES = ('FCFA', 'EUR')


def currency_preferences(request):
    selected_currency = request.session.get('currency', 'FCFA').upper()
    if selected_currency not in SUPPORTED_CURRENCIES:
        selected_currency = 'FCFA'

    return {
        'supported_currencies': SUPPORTED_CURRENCIES,
        'selected_currency': selected_currency,
        'currency_rate_eur': getattr(settings, 'CURRENCY_RATE_EUR', '655.957'),
    }
