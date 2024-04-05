from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=[('in_progress', '進行中'), ('completed', '完了')], default='in_progress')
    priority = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default='B')
    completed_at = models.DateTimeField(null=True, blank=True)  # 追加されたフィールド
    task_type = models.CharField(max_length=10, choices=(('daily', 'Daily'), ('monthly', 'Monthly')), default='')

    def __str__(self):
        return self.title
