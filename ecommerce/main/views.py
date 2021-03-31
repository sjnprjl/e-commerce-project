from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView as LV
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from django.utils.http import is_safe_url
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import FormView, RedirectView, View
from django.views.generic import ListView
from django.views import generic
from .forms import SignupForm, LoginInForm
from .models import Customer


class IndexView(TemplateView):
    template_name = "main/index.html"


class ProductView(TemplateView):
    template_name = "main/product.html"


class SearchView(TemplateView):
    template_name = "main/search.html"


class AboutUsView(TemplateView):
    template_name = "main/about_us.html"


class LoginView(LV):
    template_name = "main/account-login.html"
    authentication_form = LoginInForm
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = "/"

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class RegisterView(CreateView):
    model = Customer
    template_name = "main/account-register.html"
    form_class = SignupForm
    success_url = "/"


class PrivacyView(TemplateView):
    template_name = "main/privacy.html"


class TermsView(TemplateView):
    template_name = "main/terms.html"


class ProductWiseListView(TemplateView):
    template_name = "main/product-wise-list.html"


class App(TemplateView):
    template_name = "main/app.html"

class LogoutCustomer(TemplateView):
    template_name = "main/logout.html"

class Profile(TemplateView):
    template_name = "main/profile.html"