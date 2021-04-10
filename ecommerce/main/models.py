from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
from django.shortcuts import reverse
from django.db import models
from django.utils.html import mark_safe
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
    ourtypes = (
    ("0", "Jewlery"),
    ("1", "Furniture"),
)
  
    types = models.CharField(choices=ourtypes, max_length=2, null=False, default="Jewlery")
    description =  models.CharField(max_length=500)

    def __str__(self):
       return self.category_name

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(help_text='in Rs',)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ManyToManyField(Category)
    ourtypes = (
    ("0", "Jewellery"),
    ("1", "Furniture"),
)
  
    types = models.CharField(choices=ourtypes, max_length=2, null=False, default="Jewellery")
    Brand = models.CharField(max_length=20, null=True)
    slug = models.SlugField()
    description =  models.TextField(max_length=500)
    image = models.ImageField()
    h_image = models.ImageField()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    customer = models.ForeignKey(
    Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    customer = models.ForeignKey(
    Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
