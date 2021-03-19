from typing import Generic
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .models import * 

class index(TemplateView):
    template_name="main/index.html"
    
class product(TemplateView):
    template_name="main/product.html"

class search(TemplateView):
    template_name = "main/search.html"

class aboutus(TemplateView):
    template_name = "main/about_us.html"

class login(TemplateView):
    template_name = "main/account-login.html"
    def __init__(self, *args):
        super(login, self).__init__(*args)

class register(TemplateView):
    template_name = "main/account-register.html"
    def __init__(self, *args):
        super(register, self).__init__(*args)

class privacy(TemplateView):
    template_name = "main/privacy.html"
    def __init__(self, *args):
        super(privacy, self).__init__(*args)
    
class terms(TemplateView):
    template_name = "main/terms.html"
    def __init__(self, *args):
        super(terms, self).__init__(*args)

class product_wise_list(TemplateView):
    template_name = "main/product-wise-list.html"
    def __init__(self, *args):
        super(product_wise_list, self).__init__(*args)
        
        
        
        
