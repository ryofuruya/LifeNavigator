from django.contrib import admin
from .models import AccountBook, FixedExpense, VariableExpense

# Register your models to admin site so you can manage them through Django admin interface.
admin.site.register(AccountBook)
admin.site.register(FixedExpense)
admin.site.register(VariableExpense)
