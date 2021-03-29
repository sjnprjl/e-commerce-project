from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, full_name, password, **kwargs):
        if not email:
            raise ValueError(_("Email field is required."))
        email = self.normalize_email(email)
        user = self.model(
            email=email, user_name=user_name, full_name=full_name, **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, full_name, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")

        return self.create_user(email, user_name, full_name, password, **kwargs)


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name", "full_name"]

    objects = CustomAccountManager()

    def __str__(self):
        return self.user_name


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    description =RichTextField(blank=True, null=True)


class Product(models.Model):
    product_name = models.CharField(max_length=200, null=True)
    unit_price = models.IntegerField()
    discount = models.IntegerField()
    product_available = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = RichTextField(blank=True, null=True)
    image_field = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order_date = models.DateTimeField(auto_now_add=True)
    full_filled = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    ship_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    full_filled = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
