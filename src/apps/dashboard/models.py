from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import BaseModel
User = get_user_model()


# UserNotes model
class UserNote(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notes', verbose_name=_('User'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='added_notes', verbose_name=_('Author'), null=True, blank=True)
    text = models.TextField(_('Text'))
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('User note')
        verbose_name_plural = _('User notes')
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user} - {self.id}'
