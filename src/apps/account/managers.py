from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from django.db import models


class CustomBaseUserManager(BaseUserManager):

    def create_user(self, phonenumber, password, email=None, **extra_fields):
        """
        Create and save a normal_user with the given phonenumber and password.
        """
        if not phonenumber:
            raise ValueError(_('The phonenumber must be set'))

        user = self.model(phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_operator_user(self, phonenumber, password, email=None, **extra_fields):
        return self.create_user(phonenumber=phonenumber, password=password, role='operator_user', **extra_fields)

    def create_superuser(self, phonenumber, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields['is_phonenumber_confirmed'] = True

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phonenumber=phonenumber, password=password, role='super_user', **extra_fields)


class NormalUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role='normal_user')


class OperatorUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role='operator_user')


class SuperUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role='super_user')
