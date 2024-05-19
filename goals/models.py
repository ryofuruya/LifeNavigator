from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_type = models.CharField(max_length=50, choices=[('short_term', '短期'), ('medium_term', '中期'), ('long_term', '長期')])
    deadline = models.DateField()
    completion_status = models.BooleanField()
    achievement_percentage = models.IntegerField(default=0)  # 0-100のパーセンテージ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def goal_type(self):
        now = timezone.now().date()
        time_diff = self.deadline - now
        if time_diff < timedelta(days=365):
            return 'short_term'
        elif timedelta(days=365) <= time_diff < timedelta(days=5 * 365):
            return 'medium_term'
        else:
            return 'long_term'

    def __str__(self):
        return self.title
