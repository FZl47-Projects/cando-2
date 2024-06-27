from django import forms

from . import models


class SliderCreateForm(forms.ModelForm):
    class Meta:
        model = models.Slider
        fields = '__all__'
