from django import forms
from .models import Event
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'deadline']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        today_iso = timezone.now().date().isoformat()
        # イベント日と締切日に、今日の日付より前の日付を選択できないようにする
        self.fields['date'].widget.attrs['min'] = today_iso
        self.fields['deadline'].widget.attrs['min'] = today_iso

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError(_("タイトルは必須です。"))  # エラーメッセージを国際化
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise ValidationError(_("説明は必須です。"))  # エラーメッセージを国際化
        return description

    def clean_date(self):
        event_date = self.cleaned_data.get('date')
        if event_date is None:
            raise ValidationError(_("イベントの日付を入力してください。"))
        if event_date < timezone.now().date():
            raise ValidationError(_("イベントの日付は今日以降の日付を選択してください。"))  # 国際化されたエラーメッセージ
        return event_date

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline is None:
            raise ValidationError(_("締切日を入力してください。"))
        if deadline < timezone.now().date():
            raise ValidationError(_("締切日は今日以降の日付を選択してください。"))  # 国際化されたエラーメッセージ
        return deadline
