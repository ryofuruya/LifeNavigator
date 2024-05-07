from django import forms
from .models import Value
from django.utils.translation import gettext_lazy as _  # 国際化のサポートのためにインポート

class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError(_("タイトルは必須です。"))  # エラーメッセージをgettext_lazyで国際化
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError(_("説明は必須です。"))  # エラーメッセージをgettext_lazyで国際化
        return description
