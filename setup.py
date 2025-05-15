import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps2025.settings')
django.setup()


from django.contrib.auth.models import User
from payapp.models import UserProfile, Transaction
from converter.models import ConversionRate, create_initial_rates

def create_initial_data():
    admin, created = User.objects.get_or_create(
        username='admin1',
        defaults={
            'email': 'admin1@webapps2025.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin1')
        admin.save()
    
    UserProfile.objects.get_or_create(
        user=admin,
        defaults={
            'currency': 'GBP',
            'balance': Decimal('10000.00')
        }
    )
    print("Admin user handled")

    # test users
    test_users = [
        {'username': 'user1', 'email': 'user1@test.com', 'currency': 'GBP', 'balance': Decimal('750.00')},
        {'username': 'user2', 'email': 'user2@test.com', 'currency': 'USD', 'balance': Decimal('1000.00')},
        {'username': 'user3', 'email': 'user3@test.com', 'currency': 'EUR', 'balance': Decimal('850.00')},
    ]
    
    for user_data in test_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={'email': user_data['email']}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
       
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'currency': user_data['currency'],
                'balance': user_data['balance']
            }
        )
        print(f"User {user_data['username']} handled")

    # conversion rates
    create_initial_rates()
    print("Conversion rates created")

    Transaction.objects.all().delete()
    
    user1 = User.objects.get(username='user1')
    user2 = User.objects.get(username='user2')
    user3 = User.objects.get(username='user3')

    Transaction.objects.create(
        sender=user1,
        recipient=user2,
        amount=Decimal('100.00'),
        currency='GBP',
        transaction_type='PAYMENT',
        status='COMPLETED',
        description='Test payment 1'
    )

    Transaction.objects.create(
        sender=user2,
        recipient=user3,
        amount=Decimal('50.00'),
        currency='USD',
        transaction_type='REQUEST',
        status='PENDING',
        description='Test request 1'
    )

    print("Test transactions created")

if __name__ == '__main__':
    create_initial_data()