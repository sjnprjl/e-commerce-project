from django.views import generic
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .models import *


class IndexView(TemplateView):
    template_name = "main/index.html"


class ProductView(TemplateView):
    template_name = "main/product.html"


class SearchView(TemplateView):
    template_name = "main/search.html"


class AboutUsView(TemplateView):
    template_name = "main/about_us.html"


class LoginView(TemplateView):
    template_name = "main/account-login.html"


class RegisterView(TemplateView):
    template_name = "main/account-register.html"


class PrivacyView(TemplateView):
    template_name = "main/privacy.html"


class TermsView(TemplateView):
    template_name = "main/terms.html"


class ProductWiseListView(TemplateView):
    template_name = "main/product-wise-list.html"
