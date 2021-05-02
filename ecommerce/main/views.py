import django
from django.contrib.auth import forms
from django import http
from django.contrib.auth.forms import AuthenticationForm
from django.forms.forms import Form
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    get_user_model,
    login,
    authenticate,
    update_session_auth_hash,
)
from django.contrib.auth.views import LoginView as LV, redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.exceptions import ValidationError
from django.dispatch.dispatcher import receiver

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
from .forms import SignupForm, LoginInForm, CheckoutForm
from .models import (
    CheckoutAddress,
    Customer,
    Order,
    OrderItem,
    Category,
    Item,
    Team,
)
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
import json
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy
from allauth.account.signals import user_signed_up
from django.db.models import Q, F, DecimalField, ExpressionWrapper, Sum


def items_object():
    return Item.objects.all().annotate(
        new_price=ExpressionWrapper(
            F("price") - F("discount_price"), output_field=DecimalField()
        ),
        discount_percentage=ExpressionWrapper(
            (F("discount_price") / F("price")) * 100, output_field=DecimalField()
        ),
    )


def item_object(item):
    return item.annotate(
        new_price=ExpressionWrapper(
            F("price") - F("discount_price"), output_field=DecimalField()
        ),
        discount_percentage=ExpressionWrapper(
            (F("discount_price") / F("price")) * 100, output_field=DecimalField()
        ),
    )


ITEMS_OBJECT = items_object()


def index(request):
    cate = Category.objects.all()
    if request.user.is_authenticated:
        cart = OrderItem.objects.filter(customer=request.user)

        context = {"cate": cate, "items": ITEMS_OBJECT, "cart": cart}
    else:
        context = {"cate": cate, "items": ITEMS_OBJECT}

    # if request.user.is_authenticated:
    #     cart = OrderItem.objects.filter(customer = request.user)
    #     context = {"cart":cart}
    #     return context
    # else:
    #     None

    return render(request, "main/index.html", context)
    # def get(self, **kwargs):
    #     if self.request.user.is_authenticated:
    #         cart = OrderItem.objects.filter(customer = request.user)
    #         return render(request, "main/index.html",{'cate':cate,"items":items,"cart":cart})
    #     else:
    #         return HttpResponse("ple")


def search_view(request):
    query = request.GET.get("keyword", None)
    if query:
        items = Item.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(Brand__icontains=query)
            | Q(category__name=query)
            | Q(category__description__icontains=query)
            | Q(types__icontains=query)
        )
        item_list = serializers.serialize("json", items)
        return HttpResponse(item_list, content_type="text/json-comment-filtered")
    else:
        return HttpResponse("field is empty")


class DeleteCartItem(DeleteView):
    model = OrderItem
    success_url = reverse_lazy("cart")

    def get(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return redirect(self.get_success_url())


class PageNotFoundView(TemplateView):
    template_name = "main/404.html"


class PageNotFoundView(TemplateView):
    """404 error page view"""

    template_name = "main/404.html"


def product_view(request, pk):
    item = item_object(Item.objects).get(pk=pk)
    context = {}
    context["item"] = item
    return render(request, "main/product.html", context)


def AboutUsView(request):
    team = Team.objects.all()
    if request.user.is_authenticated:
        cart = OrderItem.objects.filter(customer=request.user)
        context = {"cart": cart, "team": team}
    else:
        context = {"team": team}

    return render(request, "main/about-page.html", context)


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
                    "redirect_url": self.get_success_url(),
                }

            return JsonResponse(data, safe=False)

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
    template_name = "main/register.html"
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


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    user.is_active = True
    user.save()


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

    pass


# class DetailCartItem(ListView):
# """detail view"""

# model = OrderItem

# template_name = "main/cart.html"

# # def get_context_data(self, **kwargs):
# #     if self.request.user.is_authenticated:
# #         context = super().get_context_data(**kwargs)
# #         context['customer'] = OrderItem.objects.filter(customer = self.request.user)
# #         return context
# #     else:
# #         None
# def get_queryset(self):
# if self.request.user.is_authenticated:
# context = OrderItem.objects.filter(customer=self.request.user)
# return context
# elif self.request.user.is_anonymous:
# return HttpResponseRedirect("/login")

# # template_name = "main/profile.html"
class DetailCartItem(LoginRequiredMixin, ListView):
    """detail view"""

    login_url = reverse_lazy("login")
    template_name = "main/cart.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return OrderItem.objects.filter(customer=self.request.user)
        else:
            None

    @staticmethod
    def get_total_price():
        total = 0
        for item in OrderItem.objects.all():
            total += item.get_final_price()
        return total

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context["carts"] = OrderItem.objects.filter(customer=self.request.user)
            context["total"] = DetailCartItem.get_total_price()
            return context
        else:
            None


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, customer=request.user, ordered=False
    )
    ordered_date = timezone.now()
    order = Order.objects.create(customer=request.user, ordered_date=ordered_date)
    return redirect(reverse_lazy("cart"))


def update_item(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    customer = request.user
    product = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, ordered=False)
    orderItem, created = OrderItem.objects.get_or_create(
        item=product, customer=customer
    )
    output = ""

    if action == "add" and orderItem.quantity < product.quantity:
        orderItem.quantity = orderItem.quantity + 1
        output = "quanity added"
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
        output = "quanity decreased"

    # save quantity of products, for an order
    orderItem.save()
    if action == "delete":
        orderItem.delete()
        output = "quanity deleted"

    if orderItem.quantity <= 0:
        # remove the orderItem from cart, when quantity reaches 0, or below it
        orderItem.delete()
        output = "quanity deleted"

    return JsonResponse(output, safe=False)


class CheckoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def get(self, *args, **kwargs):
        items = OrderItem.objects.filter(customer=self.request.user)

        context = {
            "form": CheckoutForm(
                instance=Customer.objects.get(id=self.request.user.id)
            ),
            "items": items,
            "total": DetailCartItem.get_total_price(),
        }
        return render(self.request, "main/checkout.html", context)

    def post(self, *args, **kwargs):
        pass
