from django.contrib import auth
from django.shortcuts import redirect
from django.urls import path, include
from .views import DashboardLoginVew, DashboardView
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", DashboardLoginVew.as_view(), name="Dlogin"),
    path("logout/",auth_views.LogoutView.as_view(), name="logout")

]
