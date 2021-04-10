from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="main"),
    path("app/", App.as_view(), name="app"),
    path("search/", SearchView.as_view(), name="search"),
    path("about_us/", AboutUsView.as_view(), name="about"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", Profile.as_view(), name="profile"),
    path("logout-user/", LogoutCustomer.as_view(), name="logout_user"),
    path("register/", RegisterView.as_view(), name="register"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("terms/", TermsView.as_view(), name="terms"),
    path("product/<str:pk>/", ProductView.as_view(), name="product-wise-list"),
    path("verification/", include("verify_email.urls")),
    path("activate/<str:uid>/<str:token>", Activate.as_view(), name="activate"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="main/reset_password.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="main/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="main/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="main/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path("product/<str:pk>/", ProductView.as_view(), name="product"),
    path("cart/", DetailCartItem.as_view(), name="cart"),

    path("cart/delete/<pk>/", DeleteCartItem.as_view(), name="deletecartitem"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("add-to-cart/<pk>/", add_to_cart, name="add-to-cart"),
    path("cart/update/<pk>", UpdateCartItem.as_view(), name="updatecart"),
    path("404/", PageNotFoundView.as_view(), name="404"),
]
