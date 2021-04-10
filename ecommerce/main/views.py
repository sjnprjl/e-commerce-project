
import django
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    get_user_model,
    login,
    authenticate,
    update_session_auth_hash,
)
from django.contrib.auth.views import LoginView as LV, redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError

from django.http import HttpResponseRedirect, request
from django.http.response import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import activate
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import FormView, RedirectView, View, UpdateView
from django.views.generic import ListView, DeleteView, UpdateView
from django.views import generic
from .forms import SignupForm, LoginInForm
from .models import (
    Customer,
    Order,
    OrderItem,
    Category,
    Item,)
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
from django.core.mail import EmailMessage, message
from django.urls import reverse_lazy
from .models import Customer, Item, OrderItem, Order
import json
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy


class JSONResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

        def get_data(self, context):
            return context


def index(request):
    cate = Category.objects.all()
    items = Item.objects.all()
    cart = OrderItem.objects.all()
    return render(request, "main/index.html",{'cate':cate,"items":items,"cart":cart})
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['customer'] = OrderItem.objects.filter(customer = self.request.user)
            return context
        else:
            None

class CheckOutView(TemplateView):
    template_name = "main/checkout.html"



class DetailCartItem(ListView):
    """detail view"""

    model = OrderItem
    template_name = "main/cart.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['customer'] = OrderItem.objects.filter(customer = self.request.user)
            return context
        else:
            None

class DeleteCartItem(DeleteView):
    model = OrderItem
    success_url = reverse_lazy("cart")
    def get(self, request, *args,**kwargs):
        self.delete(request,*args,**kwargs)
        return redirect(self.get_success_url())

class PageNotFoundView(TemplateView):
    template_name = "main/404.html"


class PageNotFoundView(TemplateView):
    """404 error page view"""

    template_name = "main/404.html"


class ProductView(DetailView):
    """product page view"""
    model = Item
    template_name = "main/product.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class SearchView(TemplateView):
    """search view """

    template_name = "main/search.html"


class AboutUsView(TemplateView):
    """about us view"""

    template_name = "main/about_us.html"


class Activate(View):
    """activate view"""

    def get(self, request, uid, token):

        try:
            uid = force_text(urlsafe_base64_decode(uid))
            print(uid)
            user = Customer.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("account activated succesfully")
        else:
            return HttpResponse("Activation link invalid")


class LoginView(LV, UserPassesTestMixin):
    """login view"""

    def post(self, request):
        if request.is_ajax():
            data = None
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(username=email, password=password)
            if user is None:
                data = {
                    "message": "Either username or password is incorrect",
                    "status_code": 401,
                }
            else:
                login(self.request, user)
                data = {
                    "message": "You are logged in",
                    "status_code": 200,
                    "redirect_url": self.get_success_url()
                }

            return JsonResponse(data)

    template_name = "main/login.html"
    authentication_form = LoginInForm
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = "/"
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class RegisterView(CreateView):
    """register view"""

    model = Customer
    template_name = "main/account-register.html"
    form_class = SignupForm
    success_url = "/"
    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            mail_subject = "Activate your account"
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            # activation_link = "{0}/uid/{1}&token{2}".format(current_site, uid, token)
            activation_link = reverse_lazy("activate", args=[uid, token])
            message = "Hello {0},\n {1}".format(
                user.username, str(current_site) + str(activation_link)
            )
            to_email = form.cleaned_data["email"]
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                "please confirm your  email address to be able to unlock all features"
            )
        else:
            return HttpResponse("form is invalid")


class PrivacyView(TemplateView):
    """privacy view"""

    template_name = "main/privacy.html"


class TermsView(TemplateView):
    """terms view"""

    template_name = "main/terms.html"


class ProductWiseListView(ListView):
    """product list view"""

    model = Item
    template_name = "main/product-wise-list.html"


class App(TemplateView):
    """app view"""

    template_name = "main/app.html"


class LogoutCustomer(TemplateView):
    """logout customer view"""

    template_name = "main/logout.html"


class Profile(TemplateView):
    """profile view"""

    template_name = "main/profile.html"







class UpdateCartItem(UpdateView):
    model = OrderItem
    fields = ["quantity"]
    success_url = reverse_lazy("cart")
    template_name = "main/update.html"

        


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, customer=request.user, ordered=False
    )
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect(reverse_lazy("cart"))
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect(reverse_lazy("cart"))
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            customer=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect(reverse_lazy("cart"))
