from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from payapp.models import UserProfile
from decimal import Decimal
from payapp.constants import BASE_CURRENCY, BASE_INITIAL_AMOUNT
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_initial_admin(sender, **kwargs):
    """Create initial admin user if it doesn't exist"""
    if not User.objects.filter(username='admin1').exists():
        User.objects.create_superuser('admin1', 'admin@example.com', 'admin1')

@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Safely handle UserProfile creation/update for users
    Uses get_or_create to prevent duplicate profiles
    """
    try:
       
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={
                'currency': BASE_CURRENCY,
                'balance': Decimal(str(BASE_INITIAL_AMOUNT))
            }
        )
    except Exception as e:
        logger.error(f"Error handling user profile for {instance.username}: {str(e)}")