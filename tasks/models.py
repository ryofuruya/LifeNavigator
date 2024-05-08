from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('pending', 'Pending')
    )
    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)  # 完了日を保存
    task_type = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)  # 削除されたタスクを追跡するためのフィールド
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
