from django import forms

from .models import Customer

from django.core.exceptions import ValidationError


class CustomerCreationForm(forms.ModelForm):
    confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = (
            "email",
            "username",
            "full_name",
            "address",
            "phone_number",
            "password",
            "confirm",
        )

        def clean_email(self):
            email = self.cleaned_data["email"].lower()
            r = Customer.objects.filter(email=email)
            if r.count():
                raise ValidationError("Email already exists")

            return email

        def clean_username(self):
            username = self.cleaned_data["username"].lower()
            r = Customer.objects.filter(username=username)
            if r.count():
                raise ValidationError("Username already exists")

            return username

        def clean_confirm(self):
            psd = self.cleaned_data.get("password")
            cnf = self.cleaned_data.get("confirm")

            if psd and cnf and psd != cnf:
                raise ValidationError("Password didn't match")
