from django import forms
from .models import Address


# Create Address form
class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('user', 'province', 'city', 'address_line', 'post_code')
