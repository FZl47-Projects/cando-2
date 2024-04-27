from django import forms
from . import models


class NotificationUserCreateForm(forms.ModelForm):
    class Meta:
        model = models.NotificationUser
        exclude = ('is_showing',)

    def clean(self):
        super().clean()
        if not self.is_valid():
            return

        kwargs = {}
        link_attached = self.data.get('link_attached')
        if link_attached:
            kwargs.update({
                'link_attached': link_attached,
                'link': link_attached,
            })
        self.cleaned_data['kwargs'] = kwargs
