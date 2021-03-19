from django.urls import path, include
from . import views
from .views import *
urlpatterns = [
    path("",index.as_view(), name="main"),
    path("product/", product.as_view(), name="product"),
    path("search/", search.as_view(), name="search"),
    path("about_us/", aboutus.as_view(), name="about"),
    path("login/", login.as_view(), name="login"),
    path("register/", register.as_view(), name="register"),
    path("privacy/", privacy.as_view(), name="privacy"),
    path("terms/", terms.as_view(), name="terms"),
    path("product-wise-list/", product_wise_list.as_view(), name="product-wise-list")
]
