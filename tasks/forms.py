from django import forms
from .models import Task
from django.forms import modelformset_factory, ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'deadline']
        widgets = {
            'priority': forms.Select(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("タイトルは必須です。")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise ValidationError("説明は必須です。")
        return description

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        today = timezone.now().date()  # 今日の日付を取得
        if deadline < today:
            raise ValidationError("締切日は今日以降の日付を選択してください。")
        return deadline

TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=0)

class CompletedTaskFilterForm(forms.Form):
    keyword = forms.CharField(required=False, label='キーワード', widget=forms.TextInput(attrs={'class': 'form-control'}))
    completed_date = forms.DateField(required=False, label='完了日', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def clean_keyword(self):
        keyword = self.cleaned_data.get('keyword', '').strip()
        return keyword
