from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import django.utils
from django.utils.timezone import now

CURRENT_DATE = now().strftime("%Y-%m-%d")


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, full_name, phone, isp, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not full_name:
            raise ValueError("Users must have full name")
        if not phone:
            raise ValueError("Users must have phone number")
        # if not isp:
        # raise ValueError("Users must have isp selected")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            phone=phone,
            isp=isp.set(),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, phone, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            phone=phone,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Isp(models.Model):
    isp_name = models.CharField(max_length=100)

    def __str__(self):
        return self.isp_name


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateField(verbose_name="registerd date", auto_now_add=True)
    last_login = models.DateField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    full_name = models.CharField(verbose_name="full name", max_length=50)
    phone = models.CharField(verbose_name="Phone number", max_length=20)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["full_name", "phone", "email"]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Customer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True)
    reg_date = models.DateField()
    activation = models.CharField(max_length=20, default="pending")
    exp_date = models.DateField(default=django.utils.timezone.now)
    remarks = models.CharField(max_length=200)
    isp = models.ForeignKey(Isp, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.exp_date.strftime("%Y-%m-%d") < CURRENT_DATE:
            self.activation = "expired"

        if self.exp_date.strftime("%Y-%m-%d") >= CURRENT_DATE:
            if self.activation != "pending":
                self.activation = "active"

        super().save(*args, **kwargs)


class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sub_date = models.DateField(default=django.utils.timezone.now)
    debit_amount = models.IntegerField()
    credit_amount = models.IntegerField()
    package = models.IntegerField()
    remarks = models.CharField(max_length=200)
    bill = models.CharField(max_length=20)

    def __str__(self):
        return self.customer.full_name
