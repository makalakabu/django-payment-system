from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction as db_transaction
from django.db.models import Q
from django.http import JsonResponse
from .models import UserProfile, Transaction
from django.contrib.auth.models import User
from converter.views import convert_currency
import requests
from django.core.exceptions import PermissionDenied
from decimal import Decimal

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
      
        transactions = Transaction.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).select_related('sender', 'recipient').order_by('-created_at')[:20]
        
      
        pending_requests = Transaction.objects.filter(
            recipient=request.user,
            transaction_type='REQUEST',
            status='PENDING'
        ).select_related('sender')
        
        context = {
            'profile': user_profile,
            'transactions': transactions,
            'pending_requests': pending_requests,
        }
        return render(request, 'payapp/dashboard.html', context)
    
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact admin.")
        return redirect('logout')

@login_required
def make_payment(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact admin.")
        return redirect('logout')

    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email', '').strip().lower()
        amount_str = request.POST.get('amount')
        description = request.POST.get('description', '')
        
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messages.error(request, "Amount must be positive!")
                return redirect('make_payment')
            
    
            recipient = User.objects.filter(email__iexact=recipient_email).first()
            if not recipient:
                messages.error(request, f"Recipient with email {recipient_email} not found!")
                return redirect('make_payment')
            
            if recipient == request.user:
                messages.error(request, "You cannot send money to yourself!")
                return redirect('make_payment')
            
            try:
                recipient_profile = UserProfile.objects.get(user=recipient)
            except UserProfile.DoesNotExist:
                messages.error(request, "Recipient profile not found!")
                return redirect('make_payment')
       
            if profile.balance < amount:
                messages.error(request, "Insufficient funds!")
                return redirect('make_payment')
           
            if profile.currency != recipient_profile.currency:
                conversion_url = f"http://{request.get_host()}/conversion/{profile.currency}/{recipient_profile.currency}/{amount}"
                response = requests.get(conversion_url)
                
                if response.status_code != 200:
                    messages.error(request, "Currency conversion service unavailable!")
                    return redirect('make_payment')
                
                converted_data = response.json()
                converted_amount = Decimal(converted_data['converted_amount'])
            else:
                converted_amount = amount
            
       
            with db_transaction.atomic():
                profile.balance -= amount
                recipient_profile.balance += converted_amount
                
              
                Transaction.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    amount=amount,
                    currency=profile.currency,
                    transaction_type='PAYMENT',
                    status='COMPLETED',
                    description=description
                )
                
                profile.save()
                recipient_profile.save()
                
                messages.success(request, f"Payment of {amount} {profile.currency} sent successfully!")
                return redirect('dashboard')
            
        except ValueError:
            messages.error(request, "Invalid amount!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    context = {
        'profile': profile
    }
    return render(request, 'payapp/make_payment.html', context)

@login_required
def request_payment(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact admin.")
        return redirect('logout')

    if request.method == 'POST':
        sender_email = request.POST.get('sender_email', '').strip().lower()
        amount_str = request.POST.get('amount')
        description = request.POST.get('description', '')
        
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messages.error(request, "Amount must be positive!")
                return redirect('request_payment')
            
            sender = User.objects.filter(email__iexact=sender_email).first()
            if not sender:
                messages.error(request, f"User with email {sender_email} not found!")
                return redirect('request_payment')
            
            if sender == request.user:
                messages.error(request, "You cannot request money from yourself!")
                return redirect('request_payment')
            
            try:
                sender_profile = UserProfile.objects.get(user=sender)
             
                Transaction.objects.create(
                    sender=request.user, 
                    recipient=sender,    
                    amount=amount,
                    currency=profile.currency,
                    transaction_type='REQUEST',
                    status='PENDING',
                    description=description
                )
                
                messages.success(request, f"Payment request of {amount} {profile.currency} sent successfully!")
                return redirect('dashboard')
                
            except UserProfile.DoesNotExist:
                messages.error(request, "Sender profile not found!")
        
        except ValueError:
            messages.error(request, "Invalid amount!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    context = {
        'profile': profile
    }
    return render(request, 'payapp/request_payment.html', context)

@login_required
@db_transaction.atomic
def respond_to_request(request, transaction_id, action):
  
    transaction = get_object_or_404(
        Transaction, 
        id=transaction_id, 
        recipient=request.user, 
        transaction_type='REQUEST',
        status='PENDING'
    )
    
    if action == 'accept':
        try:
            
            requester_profile = UserProfile.objects.get(user=transaction.sender)
       
            your_profile = UserProfile.objects.get(user=request.user)
            
         
            if your_profile.balance < transaction.amount:
                messages.error(request, "You don't have enough funds to fulfill this request!")
                return redirect('dashboard')
            
        
            if your_profile.currency != requester_profile.currency:
                conversion_url = f"http://{request.get_host()}/conversion/{your_profile.currency}/{requester_profile.currency}/{transaction.amount}"
                # conversion_url = f"http://127.0.0.1:8000/conversion/{your_profile.currency}/{requester_profile.currency}/{transaction.amount}"

                response = requests.get(conversion_url)
                
                if response.status_code != 200:
                    messages.error(request, "Currency conversion service unavailable!")
                    return redirect('dashboard')
                
                converted_amount = Decimal(response.json()['converted_amount'])
            else:
                converted_amount = transaction.amount
            
         
            your_profile.balance -= transaction.amount  
            requester_profile.balance += converted_amount  
            
          
            transaction.status = 'COMPLETED'
            
            your_profile.save()
            requester_profile.save()
            transaction.save()
            
            messages.success(request, f"Payment of {transaction.amount} {your_profile.currency} sent successfully!")
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    elif action == 'decline':
        transaction.status = 'DECLINED'
        transaction.save()
        messages.success(request, "Payment request declined!")
    
    return redirect('dashboard')
@staff_member_required
def admin_dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    users = User.objects.all().select_related('userprofile')
    transactions = Transaction.objects.all().order_by('-created_at')[:50]
    
    context = {
        'users': users,
        'transactions': transactions,
    }
    return render(request, 'payapp/admin_dashboard.html', context)