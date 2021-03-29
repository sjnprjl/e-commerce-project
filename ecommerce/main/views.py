from .models import Customer
from django.contrib.auth.views import LoginView
from django.views import generic
from django.views.generic import ListView, CreateView


from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .models import *

from .forms import SignupForm

class IndexView(TemplateView):
    template_name = "main/index.html"


class ProductView(TemplateView):
    template_name = "main/product.html"


class SearchView(TemplateView):
    template_name = "main/search.html"


class AboutUsView(TemplateView):
    template_name = "main/about_us.html"

class LoginView(LoginView):
    template_name = "main/account-login.html"
    
    
        
        

class RegisterView(SuccessMessageMixin,CreateView):
    form_class = SignupForm


        
    success_url = reverse_lazy('login')
    success_message = "%(user_name)s you account created sucessfully"

    

    template_name = "main/account-register.html"


class PrivacyView(TemplateView):
    template_name = "main/privacy.html"


class TermsView(TemplateView):
    template_name = "main/terms.html"


class ProductWiseListView(LoginRequiredMixin,TemplateView):
    login_url = "login"
    template_name = "main/product-wise-list.html"
