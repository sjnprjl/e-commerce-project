from typing import Generic
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .models import * 

class Index(TemplateView):
    template_name="main/index.html"

    
class Product(TemplateView):
    template_name="main/product.html"

class Search(TemplateView):
    template_name = "main/search.html"


class Aboutus(TemplateView):
    template_name = "main/about_us.html"

class Login(TemplateView):
    template_name = "main/account-login.html"

class Register(TemplateView):
    template_name = "main/account-register.html"


class Privacy(TemplateView):
    template_name = "main/privacy.html"

    
class Terms(TemplateView):
    template_name = "main/terms.html"


class Product_wise_list(TemplateView):
    template_name = "main/product-wise-list.html"

        
