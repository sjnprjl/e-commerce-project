from django.urls import path, include
from .views import *
from django.contrib import admin

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
    path("products/", ProductView.as_view(), name="product"),
    path("products-details/", ProductDetails.as_view(), name="details"),
    path("orders/", Order.as_view(), name="order"),
    path("orders-details/", OrderDetails.as_view(), name="orderdetails"),

    
]
