from django import forms
from .models import Memo
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class MemoSearchForm(forms.Form):
    keyword = forms.CharField(label=_('Search for Memos'), max_length=100, required=False, help_text=_("タイトルまたは内容で検索"))
    start_date = forms.DateField(label=_('Start Date'), required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label=_('End Date'), required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_keyword(self):
        keyword = self.cleaned_data.get('keyword', '').strip()
        return keyword

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError(_("タイトルは必須です。"))
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError(_("内容は必須です。"))
        return content
