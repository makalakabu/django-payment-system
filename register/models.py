from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from payapp.models import UserProfile
from decimal import Decimal
import requests
from django.conf import settings
from payapp.constants import BASE_CURRENCY, BASE_INITIAL_AMOUNT
import logging

logger = logging.getLogger(__name__)

class RegistrationRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registration for {self.user.username}"

def create_user_profile(user, currency=BASE_CURRENCY):
    """
    Helper function to safely create user profile
    with proper currency conversion
    """
    try:
        balance = Decimal(str(BASE_INITIAL_AMOUNT))
        
      
        if currency != BASE_CURRENCY:
            try:
                conversion_url = (
                    f"http://{settings.HOSTNAME}/conversion/"
                    f"{BASE_CURRENCY}/{currency}/{balance}"
                )
                response = requests.get(conversion_url)
                if response.status_code == 200:
                    converted_data = response.json()
                    balance = Decimal(converted_data['converted_amount'])
            except requests.RequestException as e:
                logger.warning(f"Currency conversion failed: {str(e)}. Using base currency.")


        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'currency': currency,
                'balance': balance
            }
        )
    except Exception as e:
        logger.error(f"Error creating profile for {user.username}: {str(e)}")
        raise

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    """Handle post-save actions for User model"""
    if created:
     
        if hasattr(instance, '_registration_currency'):
            create_user_profile(instance, instance._registration_currency)
            del instance._registration_currency
        else:
          
            create_user_profile(instance)