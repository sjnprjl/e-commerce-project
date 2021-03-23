from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    
    path("customers/", views.customer_view, name="customer"),
    path(
        "customers/profile/<int:customer_id>",
        views.customer_profile_view,
        name="customer_profile",
    ),
    path(
        "customers/profile/<int:customer_id>/add_subscription",
        views.customer_subscription_view,
        name="customer_subscription",
    ),
    path(
        "customers/edit/<int:customer_id>",
        views.edit_customer_view,
        name="edit_customer",
    ),
    path(
        "customers/profile/<int:customer_id>/edit_subscription/<int:subscription_id>",
        views.edit_subscription_view,
        name="edit_subscription",
    ),
    path("customers/create", views.create_customer_view, name="create_customer"),
    path("profile/", views.profile_view, name="profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("customers/delete/<int:id>/", views.delete_user, name="delete_user"),
]
