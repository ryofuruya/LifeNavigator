from django.db import models
from django.core.exceptions import ValidationError

class Value(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # タイトルの重複をチェック
        if not self.pk and Value.objects.filter(title=self.title).exists():
            raise ValidationError(f'"{self.title}" はすでに存在しています。')
        super().save(*args, **kwargs)
