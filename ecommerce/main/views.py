from typing import Generic
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .models import * 

class Index(TemplateView):
    template_name="main/index.html"
    def __init__(self, *args):
        super(Index, self).__init__(*args)
    
class Product(TemplateView):
    template_name="main/product.html"
    def __init__(self, *args):
        super(Product, self).__init__(*args)

class Search(TemplateView):
    template_name = "main/search.html"
    def __init__(self, *args):
        super(Search, self).__init__(*args)

class Aboutus(TemplateView):
    template_name = "main/about_us.html"
    def __init__(self, *args):
        super(Aboutus, self).__init__(*args)

class Login(TemplateView):
    template_name = "main/account-login.html"
    def __init__(self, *args):
        super(Login, self).__init__(*args)

class Register(TemplateView):
    template_name = "main/account-register.html"
    def __init__(self, *args):
        super(Register, self).__init__(*args)

class Privacy(TemplateView):
    template_name = "main/privacy.html"
    def __init__(self, *args):
        super(Privacy, self).__init__(*args)
    
class Terms(TemplateView):
    template_name = "main/terms.html"
    def __init__(self, *args):
        super(Terms, self).__init__(*args)

class Product_wise_list(TemplateView):
    template_name = "main/product-wise-list.html"
    def __init__(self, *args):
        super(Product_wise_list, self).__init__(*args)
        
        
        
        
