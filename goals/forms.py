from django import forms
from .models import Goal, Task
from django.utils import timezone

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # フォームがインスタンス化されるたびに、今日の日付を設定
        self.fields['deadline'].widget.attrs['min'] = timezone.now().date().isoformat()
