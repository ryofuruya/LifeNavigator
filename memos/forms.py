from django import forms
from .models import Memo

class MemoSearchForm(forms.Form):
    keyword = forms.CharField(label='Search for Memos', max_length=100, required=False)

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['title', 'content']
