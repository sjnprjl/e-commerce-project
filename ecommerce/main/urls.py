from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path("", Index.as_view(), name="main"),
    path("product/", Product.as_view(), name="product"),
    path("search/", Search.as_view(), name="search"),
    path("about_us/", AboutUs.as_view(), name="about"),
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("privacy/", Privacy.as_view(), name="privacy"),
    path("terms/", Terms.as_view(), name="terms"),
    path("product-wise-list/", ProductWiseList.as_view(), name="product-wise-list"),
]
