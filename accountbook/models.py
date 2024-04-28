from django.db import models
from django.contrib.auth.models import User

class AccountBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_entries')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100) # 例: 食費、交通費
    record_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='income')

    def __str__(self):
        return f"{self.category}: {self.amount}"

class FixedExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fixed_expenses')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)  # 例: 家賃、保険料
    description = models.TextField(blank=True, null=True)

class VariableExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='variable_expenses')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)  # 例: 食費、娯楽費
    description = models.TextField(blank=True, null=True)

class Expense(models.Model):
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category}: {self.amount} on {self.date}"