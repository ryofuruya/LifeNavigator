from django import forms
from .models import Goal, Task

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            
        }