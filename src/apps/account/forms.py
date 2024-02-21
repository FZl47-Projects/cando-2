from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django import forms

from apps.core.utils import check_phone_number, add_prefix_phonenum
from apps.account.models import UserProfile
from persiantools.jdatetime import JalaliDate


from phonenumber_field.formfields import PhoneNumberField
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phonenumber',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phonenumber',)


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phonenumber = PhoneNumberField(region='IR')
    password = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('passwords is not same')
        return p2


class RegisterUserFullForm(forms.ModelForm):
    email_error_messages = {
        'invalid': 'ایمیل نامعتبر است',
        'unique': 'این ایمیل توسط کاربر دیگه ای در حال استفاده است'
    }
    password2 = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        exclude = ('date_joined',)
        error_messages = {
            'phonenumber': {
                'invalid': 'شماره همراه نامعتبر است',
                'unique': 'کاربری با این شماره از قبل ثبت شده است'
            },
            # TODO: should add more error messages
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('رمز های عبور وارد شده بایکدیگر مغایرت دارند ')
        return p2


class ResetPasswordSetForm(forms.Form):
    phonenumber = PhoneNumberField(region='IR')
    code = forms.CharField()
    password = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('رمز های عبور وارد شده با یکدیگر مغایرت دارند')
        return p2


class UserUpdateByAdmin(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', 'is_phonenumber_confirmed', 'phonenumber', 'first_name', 'last_name')


class UpdateUserPassword(forms.Form):
    current_password = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())
    new_password2 = forms.CharField(max_length=64, min_length=8, required=True, widget=forms.PasswordInput())

    def clean_new_password2(self):
        p1 = self.cleaned_data.get('new_password')
        p2 = self.cleaned_data.get('new_password2')
        if p1 != p2:
            raise forms.ValidationError('رمز های عبور وارد شده با یکدیگر مغایرت دارند')
        return p2


# UpdateProfile form
class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput)
    last_name = forms.CharField(max_length=128, widget=forms.TextInput)
    phonenumber = forms.CharField(max_length=13, widget=forms.TextInput)

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'gender', 'image']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')

        # Convert jalali date to iso format
        if date_of_birth:
            date_of_birth = JalaliDate.to_gregorian(date_of_birth).isoformat()

        return date_of_birth

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
