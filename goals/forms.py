from django import forms
from .models import Goal, Task
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description']

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

class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # フォームがインスタンス化されるたびに、今日の日付を設定
        self.fields['deadline'].widget.attrs['min'] = timezone.now().date().isoformat()

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

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        today = timezone.now().date()
        if deadline < today:
            raise ValidationError(_("締切日は今日以降の日付を選択してください。"))  # エラーメッセージを国際化
        return deadline
