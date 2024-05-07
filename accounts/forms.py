from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import UserProfile

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'website', 'phone', 'image']

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '').strip()
        if not bio:
            raise ValidationError(_("バイオは必須です。"))  # エラーメッセージを国際化
        return bio

    def clean_website(self):
        website = self.cleaned_data.get('website', '').strip()
        if website and not website.startswith('http://') and not website.startswith('https://'):
            raise ValidationError(_("ウェブサイトのURLは有効な形式である必要があります。例: http://example.com"))
        return website

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError(_("電話番号は必須です。"))  # エラーメッセージを国際化
        return phone

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=_('Required. Inform a valid email address.'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError(_("有効なメールアドレスを入力してください。"))
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("このメールアドレスはすでに使用されています。"))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError(_("ユーザー名は必須です。"))  # エラーメッセージを国際化
        return username
