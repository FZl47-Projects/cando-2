from django.core.exceptions import ValidationError
from django import forms

from .models import UserNote


# Add UserNote form
class AddUserNoteForm(forms.ModelForm):
    class Meta:
        model = UserNote
        fields = ('user', 'author', 'text')
