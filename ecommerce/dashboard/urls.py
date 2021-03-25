from django.urls import path, include
from .views import *
from django.contrib import admin

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
]
