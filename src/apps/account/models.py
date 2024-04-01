from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from apps.product.models import WishList, Cart


class CustomBaseUserManager(BaseUserManager):

    def create_user(self, phonenumber, password, email=None, **extra_fields):
        """
        Create and save a normal_user with the given phonenumber and password.
        """
        if not phonenumber:
            raise ValueError("The phonenumber must be set")
        user = self.model(phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_operator_user(self, phonenumber, password, email=None, **extra_fields):
        return self.create_user(phonenumber=phonenumber, password=password, role='operator_user',
                                **extra_fields)

    def create_superuser(self, phonenumber, password, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields['is_phonenumber_confirmed'] = True

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phonenumber=phonenumber, password=password, role='super_user',
                                **extra_fields)


class NormalUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role='normal_user')


class OperatorUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role='operator_user')


class SuperUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role='super_user')


class User(AbstractUser):
    ROLE_USER_OPTIONS = (
        ('normal_user', 'کاربر عادی'),
        ('operator_user', 'ادمین اپراتور'),
        ('super_user', 'ادمین وِیژه'),
    )

    first_name = models.CharField("first name", max_length=150, blank=True, default="بدون نام")
    username = None
    email = None
    phonenumber = PhoneNumberField(region='IR', unique=True)
    is_phonenumber_confirmed = models.BooleanField(default=False)
    # type users|roles
    role = models.CharField(max_length=20, choices=ROLE_USER_OPTIONS, default='normal_user')

    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()
    normal_user_objects = NormalUserManager()
    operator_user_objects = OperatorUserManager()
    super_user_objects = SuperUserManager()

    class Meta:
        ordering = '-id',

    @property
    def is_admin(self):
        return True if self.role in settings.ADMIN_USER_ROLES else False

    @property
    def is_common_admin(self):
        return True if self.role in settings.COMMON_ADMIN_USER_ROLES else False

    @property
    def is_super_admin(self):
        return True if self.role in settings.SUPER_ADMIN_ROLES else False

    def __str__(self):
        return f'{self.role} - {self.phonenumber}'

    def get_role_label(self):
        return self.get_role_display()

    def get_raw_phonenumber(self):
        p = str(self.phonenumber).replace('+98', '')
        return p

    def get_full_name(self):
        fl = f'{self.first_name} {self.last_name}'.strip() or 'بدون نام'
        return fl

    def get_email(self):
        return self.email or '-'

    def get_image_url(self):
        return '/static/images/user-default-img.png'

    def get_last_login(self):
        if self.last_login:
            return self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        return '-'

    def get_current_cart(self):
        cart = Cart.objects.filter(is_active=True)
        if not cart.exists():
            cart = Cart.objects.create(user=self)
        return cart

    def get_wishlist(self):
        try:
            return self.wishlist
        except WishList.DoesNotExist:
            return WishList.objects.create(user=self)
