from django.shortcuts import render

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *


class DashboardView(LoginRequiredMixin, generic.base.TemplateView):
    login_url = "/dashboard/login/"
    template_name = "dashboard/dashboard-ecommerce.html"


class LoginView(generic.base.TemplateView):
    template_name = "dashboard/user-login.html"

class ProductView(generic.base.TemplateView):
    template_name = "dashboard/ecommerce-product-list.html"

class ProductDetails(generic.base.TemplateView):
    template_name = "dashboard/ecommerce-product-detail.html"

class Order(generic.base.TemplateView):
    template_name = "dashboard/ecommerce-order-list.html"

class OrderDetails(generic.base.TemplateView):
    template_name = "dashboard/ecommerce-order-detail.html"
