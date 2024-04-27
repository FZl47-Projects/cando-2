from django import forms

from . import models


class DefaultAddressManageForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'


class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'
