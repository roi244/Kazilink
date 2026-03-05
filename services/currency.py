from decimal import Decimal, InvalidOperation

from django.conf import settings


DEFAULT_RATES = {
    'FCFA': Decimal('1'),
    'EUR': Decimal('655.957'),
    'USD': Decimal('600'),
    'GBP': Decimal('770'),
}


def get_currency_rates():
    raw = getattr(settings, 'CURRENCY_RATES', '')
    if not raw:
        return DEFAULT_RATES.copy()

    parsed = {}
    for chunk in str(raw).split(','):
        item = chunk.strip()
        if not item or ':' not in item:
            continue

        code, value = item.split(':', 1)
        code = code.strip().upper()
        value = value.strip()

        try:
            rate = Decimal(value)
        except (InvalidOperation, ValueError):
            continue

        if code and rate > 0:
            parsed[code] = rate

    if 'FCFA' not in parsed:
        parsed['FCFA'] = Decimal('1')

    return parsed or DEFAULT_RATES.copy()


def get_supported_currencies():
    rates = get_currency_rates()
    ordered = ['FCFA']
    ordered.extend(code for code in rates.keys() if code != 'FCFA')
    return ordered
