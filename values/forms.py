from django import forms
from .models import Value

class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        fields = ['title', 'description']
