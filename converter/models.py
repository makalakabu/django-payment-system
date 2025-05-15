from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.core.validators import MinValueValidator
from payapp.constants import CURRENCY_CHOICES

class ConversionRate(models.Model):
    from_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES
    )
    to_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000001'))]
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_currency', 'to_currency')
        verbose_name = "Conversion Rate"
        verbose_name_plural = "Conversion Rates"

    def __str__(self):
        return f"1 {self.from_currency} = {self.rate} {self.to_currency}"

    def save(self, *args, **kwargs):
        if self.from_currency == self.to_currency:
            raise ValueError("Cannot create conversion rate for same currency")
        super().save(*args, **kwargs)

def create_initial_rates():
    initial_rates = [
        # GBP conversions
        {'from_currency': 'GBP', 'to_currency': 'USD', 'rate': Decimal('1.25')},
        {'from_currency': 'GBP', 'to_currency': 'EUR', 'rate': Decimal('1.17')},
        
        # USD conversions
        {'from_currency': 'USD', 'to_currency': 'GBP', 'rate': Decimal('0.80')},
        {'from_currency': 'USD', 'to_currency': 'EUR', 'rate': Decimal('0.94')},
        
        # EUR conversions
        {'from_currency': 'EUR', 'to_currency': 'GBP', 'rate': Decimal('0.85')},
        {'from_currency': 'EUR', 'to_currency': 'USD', 'rate': Decimal('1.06')},
    ]

    for rate_data in initial_rates:
        ConversionRate.objects.update_or_create(
            from_currency=rate_data['from_currency'],
            to_currency=rate_data['to_currency'],
            defaults={'rate': rate_data['rate']}
        )