from .currency import get_supported_currencies


def currency_preferences(request):
    supported = get_supported_currencies()
    selected_currency = request.session.get('currency', 'FCFA').upper()
    if selected_currency not in supported:
        selected_currency = 'FCFA'

    return {
        'supported_currencies': supported,
        'selected_currency': selected_currency,
    }
