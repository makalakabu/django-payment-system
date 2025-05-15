from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from .models import RegistrationRequest
from .forms import CustomUserCreationForm
from decimal import Decimal
import requests
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    
                    user = form.save(commit=False)
                    user.email = form.cleaned_data['email'].lower()
                    
                   
                    user._registration_currency = form.cleaned_data['currency']
                    
                    
                    user.save()
                    
                 
                    RegistrationRequest.objects.create(user=user)
                 
                    login(request, user)
                    messages.success(request, 'Registration successful! You are now logged in.')
                    return redirect('dashboard')

            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
             
                if user and user.pk:
                    user.delete()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})