from django.shortcuts import render

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *


class DashboardView(LoginRequiredMixin, generic.base.TemplateView):
    login_url = "/dashboard/login/"
    template_name = "dashboard/dashboard-ecommerce.html"


class LoginView(generic.base.TemplateView):
    template_name = "dashboard/login.html"
