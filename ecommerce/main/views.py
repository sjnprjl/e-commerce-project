import django
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, login, update_session_auth_hash
from django.contrib.auth.views import LoginView as LV
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import activate
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import FormView, RedirectView, View, UpdateView
from django.views.generic import ListView
from django.views import generic
from .forms import SignupForm, LoginInForm
from .models import Customer
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from .models import Customer

        

class IndexView(TemplateView):
    template_name = "main/index.html"


class ProductView(TemplateView):
    template_name = "main/product.html"


class SearchView(TemplateView):
    template_name = "main/search.html"


class AboutUsView(TemplateView):
    template_name = "main/about_us.html"

class Activate(View):
    def get(self, request, uid, token):

        try:
            uid = force_text(urlsafe_base64_decode(uid))
            print(uid)
            user = Customer.objects.get(pk=uid)
            
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user,token):
            user.is_active=True
            user.save()
            return HttpResponse('account activated succesfully')
        else:
            return HttpResponse('Activation link invalid')
        

class LoginView(LV, UserPassesTestMixin):

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

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
                
            
            mail_subject = 'Activate your account'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            # activation_link = "{0}/uid/{1}&token{2}".format(current_site, uid, token)
            activation_link = reverse_lazy('activate',args=[uid,token])
            message = "Hello {0},\n {1}".format(user.username, activation_link)
            to_email = form.cleaned_data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('please confirm your  email address to be able to unlock all features')
        else:
            return HttpResponse('form is invalid')
            


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