from django import forms
from .models import AccountBook, FixedExpense, VariableExpense
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AccountBookForm(forms.ModelForm):
    class Meta:
        model = AccountBook
        fields = ['category', 'amount', 'record_date', 'description']
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date'}),
        }

    amount = forms.IntegerField(
        min_value=0,  # 0 またはそれ以上の値のみ許可
        help_text='0以上の整数を入力してください。'
    )

    def __init__(self, *args, **kwargs):
        super(AccountBookForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = True
        self.fields['amount'].required = True
        self.fields['record_date'].required = True
        self.fields['description'].required = True
        self.fields['amount'].widget.attrs.update({'step': '1'})

class FixedExpenseForm(forms.ModelForm):
    record_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=localtime().date())
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'step': '1'}),
        min_value=0,  # 0以上の値のみ許可
        help_text=_('0以上の整数のみを入力してください。')
    )

    class Meta:
        model = FixedExpense
        fields = ['record_date', 'amount', 'category', 'description']

    def __init__(self, *args, **kwargs):
        super(FixedExpenseForm, self).__init__(*args, **kwargs)
        self.fields['record_date'].required = True
        self.fields['amount'].required = True
        self.fields['category'].required = True
        self.fields['description'].required = True

class VariableExpenseForm(forms.ModelForm):
    record_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=localtime().date())
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'step': '1'}),
        min_value=0,  # 0以上の値のみ許可
        help_text=_('0以上の整数のみを入力してください。')
    )

    class Meta:
        model = VariableExpense
        fields = ['record_date', 'amount', 'category', 'description']

    def __init__(self, *args, **kwargs):
        super(VariableExpenseForm, self).__init__(*args, **kwargs)
        self.fields['record_date'].required = True
        self.fields['amount'].required = True
        self.fields['category'].required = True
        self.fields['description']. required = True

class ExpenseFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category_choices = [(c, c) for c in AccountBook.objects.values_list('category', flat=True).distinct()]
    category = forms.ChoiceField(choices=category_choices, required=False)
    order_by = forms.ChoiceField(choices=[('record_date', '日付'), ('amount', '金額')], required=False)
