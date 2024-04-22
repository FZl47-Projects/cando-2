from django import forms
from . import models


class NotificationUserForm(forms.ModelForm):
    class Meta:
        model = models.NotificationUser
        exclude = ('is_showing',)
