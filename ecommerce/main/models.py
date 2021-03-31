from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, full_name, password, **kwargs):
        if not email:
            raise ValueError(_("Email field is required."))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password, **kwargs):
        kwargs.setdefault("is_admin", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_admin") is not True:
            raise ValueError("Superuser must be assigned to is_admin=True")

        return self.create_user(email, username, full_name, password, **kwargs)


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    objects = CustomAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    description = RichTextField(max_length=200)


class Product(models.Model):
    product_name = models.CharField(max_length=200, null=True)
    unit_price = models.IntegerField()
    discount = models.IntegerField()
    rating = models.IntegerField()
    product_available = models.BooleanField(default=False)
    description = RichTextField(max_length=500)
    quantity = models.IntegerField()
    image_field = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return self.product_name


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
