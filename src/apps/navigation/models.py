from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import BaseModel
User = get_user_model()


# Addresses model
class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('User'))
    province = models.CharField(_('Province'), max_length=128, null=True, blank=True)
    city = models.CharField(_('City'), max_length=128, null=True, blank=True)
    address_line = models.CharField(_('Address'), max_length=255)
    active = models.BooleanField(_('Active address'), default=False)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user} - {self.province} - {self.city}'
