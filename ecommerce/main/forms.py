from django import forms

from .models import Customer

from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import login, authenticate


class SignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )


class LoginInForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, email=username, password=password
            )
            if self.user_cache is None:
                try:
                    user_temp = Customer.objects.get(email=username, password=password)
                except:
                    user_temp = None

                if user_temp is not None:
                    self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages["invalid_login"],
                        code="invalid_login",
                        params={"username": self.username_field.verbose_name},
                    )

        return self.cleaned_data
