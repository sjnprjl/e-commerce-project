from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", IndexView.as_view(), name="main"),
    path("app/", App.as_view(), name="app"),
    path("product/", ProductView.as_view(), name="product"),
    path("search/", SearchView.as_view(), name="search"),
    path("about_us/", AboutUsView.as_view(), name="about"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("logout-user/", LogoutCustomer.as_view(), name='logout_user'),
    path("register/", RegisterView.as_view(), name="register"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("terms/", TermsView.as_view(), name="terms"),
    path("product-wise-list/", ProductWiseListView.as_view(), name="product-wise-list"),
]
