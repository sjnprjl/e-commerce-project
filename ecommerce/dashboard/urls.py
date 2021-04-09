from django.urls import path, include
from .views import *
from . import views
from django.contrib import admin

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="loginadmin"),
    path("products/", views.ProductView, name="Dproduct"),
    path("products-details/", ProductDetails.as_view(), name="details"),
    path("orders/", views.myorder, name="order"),
    path("orders-details/", OrderDetails.as_view(), name="orderdetails"),
    path("cart/", Cart.as_view(), name="Cart"),
    path("account/", Admin.as_view(), name="Admin"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
