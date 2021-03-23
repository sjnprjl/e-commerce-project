from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Account, Customer, Subscription
import re


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields["username"].error_messages = {"required": "Username is required."}
        self.fields["password"].error_messages = {"required": "Password is required."}

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]

            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Either username or password is incorrect.")


PACKAGE = [
    ("", "Select Package"),
    (1, "1 Month"),
    (2, "2 Months"),
    (3, "3 Months"),
    (4, "4 Months"),
    (5, "5 Months"),
    (6, "6 Months"),
    (7, "7 Months"),
    (8, "8 Months"),
    (9, "9 Months"),
    (10, "10 Months"),
    (11, "11 Months"),
    (12, "1 year"),
]


class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ("activation", "user", "exp_date", "package")

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        data = str(data)
        reg = "^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$"
        if re.search(reg, data) == None or len(data) < 10:
            raise ValidationError("Invalid phone number")
        return data


DEBIT_OR_CREDIT = [("D", "Debit"), ("C", "Credit")]


class SubscriptionForm(forms.ModelForm):
    debit_or_credit_radio = forms.ChoiceField(
        required=True, widget=forms.RadioSelect, choices=DEBIT_OR_CREDIT, initial="C"
    )
    package = forms.ChoiceField(required=True, choices=PACKAGE, widget=forms.Select())
    amount = forms.IntegerField(required=True)

    class Meta:
        model = Subscription
        fields = "__all__"
        exclude = (
            "customer",
            "exp_date",
            "balance_amount",
        )

    def clean_amount(self):
        data = self.cleaned_data["amount"]
        data = str(data)
        if not data.isnumeric():
            raise ValidationError("Invalid amount.")
        return data
