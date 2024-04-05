from django import forms
from .models import AccountBook, FixedExpense, VariableExpense
from django.utils.timezone import localtime
from .models import AccountBook


class AccountBookForm(forms.ModelForm):
    record_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=localtime().date())

    class Meta:
        model = AccountBook
        fields = ['amount', 'category', 'record_date', 'description']

class FixedExpenseForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=localtime().date())

    class Meta:
        model = FixedExpense
        fields = ['payment_date', 'amount', 'category', 'description']

class VariableExpenseForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=localtime().date())

    class Meta:
        model = VariableExpense
        fields = ['payment_date', 'amount', 'category', 'description']

class ExpenseFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category_choices = [(c, c) for c in AccountBook.objects.values_list('category', flat=True).distinct()]
    category = forms.ChoiceField(choices=category_choices, required=False)
    order_by = forms.ChoiceField(choices=[('record_date', '日付'), ('amount', '金額')], required=False)