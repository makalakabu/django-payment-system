from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from payapp.constants import CURRENCY_CHOICES

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        initial='GBP',
        help_text="Select your account currency"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "currency")

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email