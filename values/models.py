from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Value(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # タイトルの重複をチェック
        if not self.pk and Value.objects.filter(title=self.title).exists():
            raise ValidationError(f'"{self.title}" はすでに存在しています。')
        super().save(*args, **kwargs)
