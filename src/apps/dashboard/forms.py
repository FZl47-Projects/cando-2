from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django import forms

from apps.core.utils import check_phone_number, add_prefix_phonenum
from apps.account.models import UserProfile


# UpdateProfile form
class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput)
    last_name = forms.CharField(max_length=128, widget=forms.TextInput)
    phonenumber = forms.CharField(max_length=13, widget=forms.TextInput)

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'image']

    def clean(self):
        phone_number = self.cleaned_data.get('phonenumber')

        # Validate phone number
        if not check_phone_number(phone_number):
            raise ValidationError(_('Enter a valid phone number'), code='BAD-PHONE-NUMBER')

    def save(self, commit=True):
        profile = super().save(commit)
        user = profile.user

        # Update user data
        user.phonenumber = add_prefix_phonenum(self.cleaned_data.get('phonenumber'))
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        profile.save()
        return profile
