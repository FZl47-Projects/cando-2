from django import forms

from . import models


class InvoiceCreateForm(forms.ModelForm):


    class Meta:
        model = models.Invoice
        fields = '__all__'
