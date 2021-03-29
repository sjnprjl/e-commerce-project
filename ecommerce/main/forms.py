from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = [
            'user_name',
            'full_name',
            
            'email',
            'password1',
            'password2',

            
        ]