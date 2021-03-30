from django import forms

from .models import Customer

from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm
class SignupForm(UserCreationForm):
  
    class Meta:
        model = Customer
        fields = [
            "email",
            "username",
            "password1",
            "password2",
        ]

        
