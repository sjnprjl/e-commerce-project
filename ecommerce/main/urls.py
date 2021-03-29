from django.contrib import auth
from django.urls import path, include
from .views import *
from .models import Customer
from django.contrib.auth import logout, views as auth_views

urlpatterns = [
    path("", IndexView.as_view(), name="main"),
    path("product/", ProductView.as_view(), name="product"),
    path("search/", SearchView.as_view(), name="search"),
    path("about_us/", AboutUsView.as_view(), name="about"),
    path("logout/",auth_views.LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(),name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("terms/", TermsView.as_view(), name="terms"),
    path("product-wise-list/", ProductWiseListView.as_view(), name="product-wise-list"),
]
