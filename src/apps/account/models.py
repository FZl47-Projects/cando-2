from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.templatetags.static import static
from django.shortcuts import reverse
from django.conf import settings
from django.db import models
from . import managers
from . import enums
from phonenumber_field.modelfields import PhoneNumberField


# Custom User model
class User(AbstractUser):
    Roles = enums.UserRolesEnum

    first_name = models.CharField(_('First name'), max_length=128, blank=True, default=_('No name'))
    username = None
    email = None
    phonenumber = PhoneNumberField(verbose_name=_('Phone number'), region='IR', unique=True)
    is_phonenumber_confirmed = models.BooleanField(_('Is confirmed'), default=False)
    role = models.CharField(_('User role'), max_length=32, choices=Roles.choices, default=Roles.NORMAL)

    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = []

    objects = managers.CustomBaseUserManager()
    normal_user_objects = managers.NormalUserManager()
    operator_user_objects = managers.OperatorUserManager()
    super_user_objects = managers.SuperUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.role} - {self.get_raw_phonenumber()}'

    @property
    def is_admin(self):
        return True if self.role in settings.ADMIN_USER_ROLES else False

    @property
    def is_common_admin(self):
        return True if self.role in settings.COMMON_ADMIN_USER_ROLES else False

    @property
    def is_super_admin(self):
        return True if self.role in settings.SUPER_ADMIN_ROLES else False

    def get_role_label(self):
        return self.get_role_display()

    def get_raw_phonenumber(self):
        p = str(self.phonenumber).replace('+98', '')
        return p

    def get_phone_number(self):
        return str(self.phonenumber).replace('+98', '0')

    def get_full_name(self):
        fl = f'{self.first_name} {self.last_name}'.strip() or _('No name')
        return fl

    def get_image_url(self):
        return '/static/images/dashboard/client_img.png'

    def get_last_login(self):
        if self.last_login:
            return self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        return '-'

    def get_dashboard_url(self):
        if self.is_admin:
            return reverse('dashboard:admin')
        return reverse('dashboard:user')


# Users' Profile model
class UserProfile(models.Model):
    Genders = enums.UserGendersEnum

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    melli_code = models.CharField(_('Melli code'), max_length=10, null=True, blank=True)
    gender = models.CharField(_('Gender'), max_length=16, choices=Genders.choices, default=Genders.UNKNOWN)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    image = models.ImageField(_('Profile picture'), upload_to='images/profiles/', null=True, blank=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.get_raw_phonenumber()}'

    def get_image_url(self):
        if self.image:
            return self.image.url
        return static('images/user-default.png')

    def get_gender_label(self):
        return self.get_gender_display()

    def get_date_of_birth(self):
        if self.date_of_birth:
            return self.date_of_birth.strftime('%Y-%m-%d')
