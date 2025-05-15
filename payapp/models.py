from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from payapp.constants import CURRENCY_CHOICES

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='GBP'
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def formatted_balance(self):
        from payapp.constants import CURRENCY_SYMBOLS
        symbol = CURRENCY_SYMBOLS.get(self.currency, '')
        return f"{symbol}{self.balance:.2f}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('PAYMENT', 'Payment'),
        ('REQUEST', 'Request'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('DECLINED', 'Declined'),
    ]
    
    sender = models.ForeignKey(
        User, 
        related_name='sent_transactions', 
        on_delete=models.PROTECT
    )
    recipient = models.ForeignKey(
        User, 
        related_name='received_transactions', 
        on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} from {self.sender} to {self.recipient} - {self.amount} {self.currency}"
    
    @property
    def formatted_amount(self):
        from payapp.constants import CURRENCY_SYMBOLS
        symbol = CURRENCY_SYMBOLS.get(self.currency, '')
        return f"{symbol}{self.amount:.2f}"