from django.utils.translation import gettext_lazy as _

CURRENCY_CHOICES = [
    ('GBP', _('British Pound (£)')),
    ('USD', _('US Dollar ($)')),
    ('EUR', _('Euro (€)')),
]

CURRENCY_SYMBOLS = {
    'GBP': '£',
    'USD': '$',
    'EUR': '€',
}

BASE_CURRENCY = 'GBP'
BASE_INITIAL_AMOUNT = 750.00