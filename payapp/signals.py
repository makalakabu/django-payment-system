from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from decimal import Decimal
from payapp.constants import BASE_CURRENCY, BASE_INITIAL_AMOUNT

@receiver(post_save, sender=User)
def create_initial_admin(sender, **kwargs):
    if not User.objects.filter(username='admin1').exists():
        User.objects.create_superuser('admin1', 'admin@example.com', 'admin1')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(
            user=instance,
            currency=BASE_CURRENCY,
            balance=Decimal(str(BASE_INITIAL_AMOUNT))
        )