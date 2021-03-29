from django.shortcuts import render

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import *

class DashboardLoginVew(LoginView):
    template_name='dashboard/login.html'


class DashboardView(LoginRequiredMixin, generic.base.TemplateView):
    login_url = "/dashboard/login/"
    template_name = "dashboard/dashboard-ecommerce.html"


