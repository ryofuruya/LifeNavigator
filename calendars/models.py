# models.py

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Task(models.Model):
    # 既存のフィールド
    deadline = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    # 追加するフィールド
    is_deleted = models.BooleanField(default=False)