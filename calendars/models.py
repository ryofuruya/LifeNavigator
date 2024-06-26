from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    deadline = models.DateField(default=timezone.now)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  

    def __str__(self):
        return self.title

class Task(models.Model):
    # 既存のフィールド
    deadline = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    # 追加するフィールド
    is_deleted = models.BooleanField(default=False)