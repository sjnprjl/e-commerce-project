from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as LV
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic.base import TemplateView
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    login as auth_login,
    logout as auth_logout,
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, QueryDict


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = "/dashboard/login/"
    template_name = "dashboard/dashboard-ecommerce.html"


class LoginView(LV, UserPassesTestMixin):
    """
    Provides the ability to login as a user with a username and password
    """

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    template_name = "dashboard/user-login.html"
    success_url = "/dashboard/"
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if (
            self.redirect_authenticated_user
            and self.request.user.is_authenticated
            and self.request.user.is_staff
        ):
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """

    url = "/dashboard/login/"

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ProductView(TemplateView):
    template_name = "dashboard/ecommerce-product-list.html"


class ProductDetails(TemplateView):
    template_name = "dashboard/ecommerce-product-detail.html"


class Order(TemplateView):
    template_name = "dashboard/ecommerce-order-list.html"


class OrderDetails(TemplateView):
    template_name = "dashboard/ecommerce-order-detail.html"


class Cart(TemplateView):
    template_name = "dashboard/ecommerce-cart.html"


class Admin(TemplateView):
    template_name = "dashboard/ecommerce-myaccount.html"
