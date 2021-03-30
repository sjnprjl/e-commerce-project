from django.views import generic
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin

from main.forms import CustomerCreationForm
from main.models import Customer

from django.views.generic import FormView, RedirectView


class IndexView(TemplateView):
    template_name = "main/index.html"


class ProductView(TemplateView):
    template_name = "main/product.html"


class SearchView(TemplateView):
    template_name = "main/search.html"


class AboutUsView(TemplateView):
    template_name = "main/about_us.html"


class LoginView(FormView):
    template_name = "main/account-login.html"


class RegisterView(FormView):
    model = Customer
    template_name = "main/account-register.html"
    form_class = CustomerCreationForm
    success_url = '/'




class PrivacyView(TemplateView):
    template_name = "main/privacy.html"


class TermsView(TemplateView):
    template_name = "main/terms.html"


class ProductWiseListView(TemplateView):
    template_name = "main/product-wise-list.html"


class App(TemplateView):
    template_name = "main/app.html"
