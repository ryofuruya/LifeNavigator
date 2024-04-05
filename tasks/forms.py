from django import forms
from .models import Task
from django.forms import modelformset_factory

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'priority', 'title']
        widgets = {
            'status': forms.Select(),
            'priority': forms.Select(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=0)

class CompletedTaskFilterForm(forms.Form):
    keyword = forms.CharField(required=False, label='キーワード')
    completed_date = forms.DateField(required=False, label='完了日', widget=forms.DateInput(attrs={'type': 'date'}))
