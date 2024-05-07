from django import forms
from accounts.models import UserProfile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'website', 'phone', 'image']

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '').strip()
        if not bio:
            raise ValidationError(_("バイオは必須です。"))  # 国際化されたエラーメッセージを追加
        return bio

    def clean_website(self):
        website = self.cleaned_data.get('website', '').strip()
        if website and not website.startswith('http://') and not website.startswith('https://'):
            raise ValidationError(_("ウェブサイトのURLは有効な形式である必要があります。例: http://example.com"))
        if not website:
            raise ValidationError(_("ウェブサイトは必須です。"))  # 必須である場合に対応
        return website

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError(_("電話番号は必須です。"))  # 必須である場合のエラーメッセージを追加
        return phone
