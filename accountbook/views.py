from django.shortcuts import render, redirect, get_object_or_404
from .models import AccountBook, FixedExpense, VariableExpense, Expense
from django.contrib.auth.decorators import login_required
from .forms import AccountBookForm, FixedExpenseForm, VariableExpenseForm, ExpenseFilterForm
from django.db.models import Sum
from django.utils import timezone
import pytz
import calendar
import datetime  # datetimeモジュールをインポート
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import AccountBook, FixedExpense, VariableExpense, Expense, Income, Outflow


@login_required
def accountbook_list(request):
    form = ExpenseFilterForm(request.GET)
    records = AccountBook.objects.filter(user=request.user)
    
    if form.is_valid():
        if form.cleaned_data.get('start_date'):
            records = records.filter(record_date__gte=form.cleaned_data['start_date'])
        if form.cleaned_data.get('end_date'):
            records = records.filter(record_date__lte=form.cleaned_data['end_date'])
        if form.cleaned_data.get('category'):
            records = records.filter(category=form.cleaned_data['category'])
        if form.cleaned_data.get('order_by'):
            records = records.order_by(form.cleaned_data['order_by'])

    now = timezone.now()
    month_start = timezone.datetime(now.year, now.month, 1)
    month_end = timezone.datetime(now.year, now.month + 1, 1) if now.month < 12 else timezone.datetime(now.year + 1, 1, 1)

    incomes = AccountBook.objects.filter(user=request.user, record_date__range=(month_start, month_end), type='income')
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    total_variable_expense = VariableExpense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_fixed_expense = FixedExpense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = total_variable_expense + total_fixed_expense

    net_income = total_income - total_expense
    
    context = {
        'records': records,
        'form': form,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': net_income,
    }
    return render(request, 'accountbook/accountbook_list.html', context)

@login_required
def add_account_entry(request):
    if request.method == 'POST':
        form = AccountBookForm(request.POST)
        if form.is_valid():
            account_entry = form.save(commit=False)
            account_entry.user = request.user
            account_entry.record_date = timezone.now()
            account_entry.save()
            return redirect('accountbook:accountbook_list')
    else:
        form = AccountBookForm()
    return render(request, 'accountbook/add_entry.html', {'form': form})

@login_required
def summary_view(request):
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    selected_month = request.GET.get('month', current_month)

    # 月の選択肢を作成します
    months = [{'value': i, 'display': calendar.month_name[i]} for i in range(1, 13)]

    # 月別の収入と支出を計算します
    monthly_incomes = AccountBook.objects.filter(
        user=request.user,
        record_date__year=current_year,
        record_date__month=selected_month,
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = VariableExpense.objects.filter(
        user=request.user,
        record_date__year=current_year,
        record_date__month=selected_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_fixed_expenses = FixedExpense.objects.filter(
        user=request.user,
        record_date__year=current_year,
        record_date__month=selected_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_monthly_outflow = monthly_expenses + monthly_fixed_expenses

    net_income = monthly_incomes - total_monthly_outflow

    context = {
        'monthly_incomes': monthly_incomes,
        'total_monthly_outflow': total_monthly_outflow,
        'net_income': net_income,
        'months': months,
        'selected_month': int(selected_month),  # 選択された月を整数として渡します
    }

    return render(request, 'accountbook/summary_view.html', context)

@login_required
def add_variable_expense(request):
    if request.method == 'POST':
        form = VariableExpenseForm(request.POST)
        if form.is_valid():
            variable_expense = form.save(commit=False)
            variable_expense.user = request.user
            variable_expense.save()
            return redirect('accountbook:variable_expense_list')
        else:
            return render(request, 'accountbook/add_variable_expense.html', {'form': form, 'errors': form.errors})
    else:
        form = VariableExpenseForm()
    return render(request, 'accountbook/add_variable_expense.html', {'form': form})

@login_required
def add_income(request):
    if request.method == 'POST':
        form = AccountBookForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('accountbook:income_list')
    else:
        form = AccountBookForm()
    return render(request, 'accountbook/add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = VariableExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('accountbook:accountbook_list')
    else:
        form = VariableExpenseForm()
    return render(request, 'accountbook/add_expense.html', {'form': form})

@login_required
def income_list(request):
    now = timezone.now()
    month_start = timezone.datetime(now.year, now.month, 1)
    month_end = timezone.datetime(now.year, now.month + 1, 1) if now.month < 12 else timezone.datetime(now.year + 1, 1, 1)
    
    incomes = AccountBook.objects.filter(user=request.user, record_date__range=(month_start, month_end), type='income')
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'incomes': incomes,
        'total_income': total_income,
    }
    
    return render(request, 'accountbook/income_list.html', context)

@login_required
def variable_expense_list(request):
    now = timezone.now()
    month_start = timezone.datetime(now.year, now.month, 1)
    month_end = timezone.datetime(now.year, now.month + 1, 1) if now.month < 12 else timezone.datetime(now.year + 1, 1, 1)

    variable_expenses = VariableExpense.objects.filter(user=request.user, record_date__range=(month_start, month_end))
    total_variable_expense = variable_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'variable_expenses': variable_expenses,
        'total_variable_expense': total_variable_expense,
    }
    
    return render(request, 'accountbook/variable_expense_list.html', context)

@login_required
def expense_list(request):
    now = timezone.now()
    utc_tz = pytz.UTC
    current_month_start = datetime.datetime(now.year, now.month, 1, tzinfo=utc_tz)
    if now.month == 12:
        current_month_end = datetime.datetime(now.year + 1, 1, 1, tzinfo=utc_tz)
    else:
        current_month_end = datetime.datetime(now.year, now.month + 1, 1, tzinfo=utc_tz)

    variable_expenses = VariableExpense.objects.filter(user=request.user, record_date__range=(current_month_start, current_month_end))
    total_variable_expenses = variable_expenses.aggregate(total=Sum('amount'))['total'] or 0

    fixed_expenses = FixedExpense.objects.filter(user=request.user, record_date__range=(current_month_start, current_month_end))
    total_fixed_expenses = fixed_expenses.aggregate(total=Sum('amount'))['total'] or 0

    total_expenses = total_variable_expenses + total_fixed_expenses

    context = {
        'variable_expenses': variable_expenses,
        'fixed_expenses': fixed_expenses,
        'total_variable_expenses': total_variable_expenses,
        'total_fixed_expenses': total_fixed_expenses,
        'total_expenses': total_expenses,
    }
    return render(request, 'accountbook/expense_list.html', context)

@login_required
def current_month_fixed_expenses(request):
    now = timezone.now()
    month_start = timezone.datetime(now.year, now.month, 1)
    month_end = timezone.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])
    
    fixed_expenses = FixedExpense.objects.filter(user=request.user, record_date__range=(month_start, month_end))
    
    context = {'fixed_expenses': fixed_expenses}
    return render(request, 'accountbook/current_month_fixed_expenses.html', context)

@login_required
def monthly_fixed_expenses(request):
    now = timezone.now()
    current_month_start = timezone.datetime(now.year, now.month, 1)
    current_month_end = timezone.datetime(now.year, now.month + 1, 1) - timezone.timedelta(seconds=1)

    fixed_expenses = FixedExpense.objects.filter(user=request.user, record_date__range=(current_month_start, current_month_end))
    total_expenses = fixed_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'expenses': fixed_expenses,
        'total_expenses': total_expenses,
    }
    return render(request, 'accountbook/monthly_fixed_expenses.html', context)

@login_required
def income_summary_view(request):
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    
    current_month_start = datetime.datetime(current_year, current_month, 1, tzinfo=pytz.UTC)
    if current_month == 12:
        current_month_end = datetime.datetime(current_year + 1, 1, 1, tzinfo=pytz.UTC) - datetime.timedelta(seconds=1)
    else:
        current_month_end = datetime.datetime(current_year, current_month + 1, 1, tzinfo=pytz.UTC) - datetime.timedelta(seconds=1)

    monthly_fixed_expenses = FixedExpense.objects.filter(user=request.user, record_date__year=current_year, record_date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0
    monthly_expenses = VariableExpense.objects.filter(user=request.user, record_date__year=current_year, record_date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0
    
    total_income = AccountBook.objects.filter(user=request.user, record_date__year=current_year, record_date__month=current_month, type='income').aggregate(total=Sum('amount'))['total'] or 0

    monthly_income = AccountBook.objects.filter(
        user=request.user,
        record_date__range=(current_month_start, current_month_end),
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    yearly_income = AccountBook.objects.filter(
        user=request.user,
        record_date__year=current_year,
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    previous_month = current_month - 1 if current_month > 1 else 12
    previous_year = current_year if current_month > 1 else current_year - 1
    previous_month_start = datetime.datetime(previous_year, previous_month, 1, tzinfo=pytz.UTC)
    previous_month_end = previous_month_start + datetime.timedelta(days=calendar.monthrange(previous_year, previous_month)[1]) - datetime.timedelta(seconds=1)

    previous_month_income = AccountBook.objects.filter(
        user=request.user,
        record_date__range=(previous_month_start, previous_month_end),
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    previous_year_income = AccountBook.objects.filter(
        user=request.user,
        record_date__year=previous_year,
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'monthly_fixed_expenses': monthly_fixed_expenses,
        'monthly_expenses': monthly_expenses,
        'total_income': total_income,
        'monthly_income': monthly_income,
        'yearly_income': yearly_income,
        'previous_month_income': previous_month_income,
        'previous_year_income': previous_year_income,
    }

    return render(request, 'accountbook/income_summary_view.html', context)

@csrf_exempt
@require_POST
def update_income(request):
    data = json.loads(request.body)
    income_id = data.get('id')
    field = data.get('field')
    value = data.get('value')

    if field == 'record_date':
        value = parse_date(value)

    income = get_object_or_404(AccountBook, id=income_id, user=request.user)
    setattr(income, field, value)
    income.save()

    return JsonResponse({'status': 'success'})

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(AccountBook, id=income_id, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('accountbook:income_list')
    return render(request, 'common/delete_confirm.html', {'object': income, 'cancel_url': reverse('accountbook:income_list')})

@login_required
def delete_variable_expense(request, expense_id):
    expense = get_object_or_404(VariableExpense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('accountbook:variable_expense_list')
    return render(request, 'common/delete_confirm.html', {'object': expense, 'cancel_url': reverse('accountbook:variable_expense_list')})

@login_required
def delete_fixed_expense(request, expense_id):
    expense = get_object_or_404(FixedExpense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('accountbook:monthly_fixed_expenses')
    return render(request, 'common/delete_confirm.html', {'object': expense, 'cancel_url': reverse('accountbook:monthly_fixed_expenses')})

@csrf_exempt
@require_POST
def update_variable_expense(request):
    data = json.loads(request.body)
    expense_id = data.get('id')
    field = data.get('field')
    value = data.get('value')

    expense = get_object_or_404(VariableExpense, id=expense_id, user=request.user)

    if field == 'amount':
        value = int(round(float(value)))

    setattr(expense, field, value)
    expense.save()

    return JsonResponse({'status': 'success'})

@csrf_exempt
@require_POST
def update_fixed_expense(request):
    data = json.loads(request.body)
    expense_id = data.get('id')
    field = data.get('field')
    value = data.get('value')

    expense = get_object_or_404(FixedExpense, id=expense_id, user=request.user)

    if field == 'amount':
        value = int(round(float(value)))

    setattr(expense, field, value)
    expense.save()

    return JsonResponse({'status': 'success'})

@require_POST
@csrf_exempt
def update_expense(request):
    try:
        data = json.loads(request.body)
        expense = get_object_or_404(Expense, id=data['id'], user=request.user)
        setattr(expense, data['field'], data['value'])
        expense.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def edit_account_book(request, model_type, id):
    model_classes = {
        'income': AccountBook,
        'variable_expense': VariableExpense,
        'monthly_fixed_expense': FixedExpense
    }
    model = model_classes.get(model_type)
    if not model:
        raise Http404("Account type not found.")

    instance = get_object_or_404(model, pk=id, user=request.user)
    if request.method == 'POST':
        form = AccountBookForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('accountbook:detail_account_book', model_type=model_type, id=id)
    else:
        form = AccountBookForm(instance=instance)
        # Amountフィールドの値を整数にキャスト
        if 'Amount' in form.fields:
            form.initial['Amount'] = int(form.initial['Amount'])

    context = {
        'form': form,
        'model_type': model_type,
        'instance': instance,
    }
    return render(request, 'accountbook/account_book_edit.html', context)

@login_required
def detail_account_book(request, model_type, id):
    model_classes = {
        'income': AccountBook,
        'variable_expense': VariableExpense,
        'monthly_fixed_expense': FixedExpense
    }

    model = model_classes.get(model_type)
    if not model:
        raise Http404("Account type not found.")

    instance = get_object_or_404(model, pk=id, user=request.user)

    context = {
        'instance': instance,
        'model_type': model_type
    }
    return render(request, 'accountbook/detail_account_book.html', context)

@login_required
def add_fixed_expense(request):
    if request.method == 'POST':
        form = FixedExpenseForm(request.POST)
        if form.is_valid():
            fixed_expense = form.save(commit=False)
            fixed_expense.user = request.user
            fixed_expense.save()
            return redirect('accountbook:monthly_fixed_expenses')
        else:
            return render(request, 'accountbook/add_fixed_expense.html', {'form': form})
    else:
        form = FixedExpenseForm()
    return render(request, 'accountbook/add_fixed_expense.html', {'form': form})
