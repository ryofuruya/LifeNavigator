from django.shortcuts import render, redirect, get_object_or_404
from .models import AccountBook,FixedExpense, VariableExpense, Expense
from django.contrib.auth.decorators import login_required
from .forms import AccountBookForm, FixedExpenseForm, VariableExpenseForm, ExpenseFilterForm, FixedExpense
from django.db.models import Sum, F
from django.utils.timezone import now
from django.utils import timezone
from .forms import ExpenseFilterForm
import datetime
import pytz
import calendar
from django.db.models.functions import TruncMonth, TruncYear
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

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

    incomes = AccountBook.objects.filter(user=request.user, record_date__range=(month_start, month_end))
    # 収入合計
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    # 支出合計 (変動費と固定費を合算)
    total_variable_expense = VariableExpense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_fixed_expense = FixedExpense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = total_variable_expense + total_fixed_expense

    # 純収入
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
    current_month = now().month
    current_year = now().year
    
    # 月別集計
    monthly_expenses = VariableExpense.objects.filter(user=request.user, payment_date__year=current_year, payment_date__month=current_month).aggregate(total=Sum('amount'))
    monthly_fixed_expenses = FixedExpense.objects.filter(user=request.user, payment_date__year=current_year, payment_date__month=current_month).aggregate(total=Sum('amount'))
    
    # 年別集計
    yearly_expenses = VariableExpense.objects.filter(user=request.user, payment_date__year=current_year).aggregate(total=Sum('amount'))
    yearly_fixed_expenses = FixedExpense.objects.filter(user=request.user, payment_date__year=current_year).aggregate(total=Sum('amount'))
    
    # 前月の集計
    previous_month = current_month - 1 if current_month > 1 else 12
    previous_year = current_year if current_month > 1 else current_year - 1
    previous_month_expenses = VariableExpense.objects.filter(
        user=request.user, 
        payment_date__year=previous_year, 
        payment_date__month=previous_month
    ).aggregate(total=Sum('amount'))
    previous_month_fixed_expenses = FixedExpense.objects.filter(
        user=request.user, 
        payment_date__year=previous_year, 
        payment_date__month=previous_month
    ).aggregate(total=Sum('amount'))
    
    # 前年の集計
    previous_year_expenses = VariableExpense.objects.filter(
        user=request.user,
        payment_date__year=current_year - 1
    ).aggregate(total=Sum('amount'))
    previous_year_fixed_expenses = FixedExpense.objects.filter(
        user=request.user,
        payment_date__year=current_year - 1
    ).aggregate(total=Sum('amount'))
    
    # 変化率の計算
    def calculate_change(current, previous):
        if previous and previous['total']:
            return (current['total'] or 0) - (previous['total'] or 0)
        return 0
    
    # 前月比、前年比の変化量の計算
    monthly_expense_change = calculate_change(monthly_expenses, previous_month_expenses)
    yearly_expense_change = calculate_change(yearly_expenses, previous_year_expenses)
    monthly_fixed_expense_change = calculate_change(monthly_fixed_expenses, previous_month_fixed_expenses)
    yearly_fixed_expense_change = calculate_change(yearly_fixed_expenses, previous_year_fixed_expenses)
    
    context = {
        'monthly_expenses': monthly_expenses['total'],
        'monthly_fixed_expenses': monthly_fixed_expenses['total'],
        'yearly_expenses': yearly_expenses['total'],
        'yearly_fixed_expenses': yearly_fixed_expenses['total'],
        'monthly_expense_change': monthly_expense_change,
        'previous_month_expenses': previous_month_expenses,
        'previous_month_fixed_expenses': previous_month_fixed_expenses,
        'previous_year_expenses': previous_year_expenses,
        'previous_year_fixed_expenses': previous_year_fixed_expenses,
    }
    
    return render(request, 'accountbook/summary_view.html', context)

@login_required
def add_fixed_expense(request):
    if request.method == 'POST':
        form = FixedExpenseForm(request.POST)
        if form.is_valid():
            fixed_expense = form.save(commit=False)
            fixed_expense.user = request.user
            fixed_expense.payment_date = timezone.now()  # 現在の日時を設定
            fixed_expense.save()
            return redirect('accountbook:monthly_fixed_expenses')
    else:
        form = FixedExpenseForm()
    return render(request, 'accountbook/add_fixed_expense.html', {'form': form})

@login_required
def add_variable_expense(request):
    if request.method == 'POST':
        form = VariableExpenseForm(request.POST)
        if form.is_valid():
            variable_expense = form.save(commit=False)
            variable_expense.user = request.user
            variable_expense.payment_date = timezone.now()  # 現在の日時を設定
            variable_expense.save()
            return redirect('accountbook:variable_expense_list')
    else:
        form = VariableExpenseForm()
    return render(request, 'accountbook/add_variable_expense.html', {'form': form})

# 収入登録ビュー
@login_required
def add_income(request):
    if request.method == 'POST':
        form = AccountBookForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('accountbook:accountbook_list')
    else:
        form = AccountBookForm()
    return render(request, 'accountbook/add_income.html', {'form': form})

# 支出登録ビュー
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
    # 当月を取得
    now = timezone.now()
    month_start = timezone.datetime(now.year, now.month, 1)
    month_end = timezone.datetime(now.year, now.month + 1, 1) if now.month < 12 else timezone.datetime(now.year + 1, 1, 1)
    
    # 当月の収入データをフィルタリング
    incomes = AccountBook.objects.filter(user=request.user, record_date__range=(month_start, month_end))
    
    # 合計金額を計算
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

    # 当月の変動費データをフィルタリング
    variable_expenses = VariableExpense.objects.filter(user=request.user, payment_date__range=(month_start, month_end))
    
    # 合計金額を計算
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

    variable_expenses = VariableExpense.objects.filter(user=request.user, payment_date__range=(current_month_start, current_month_end))
    total_variable_expenses = variable_expenses.aggregate(total=Sum('amount'))['total'] or 0

    fixed_expenses = FixedExpense.objects.filter(user=request.user, payment_date__range=(current_month_start, current_month_end))
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
    
    fixed_expenses = FixedExpense.objects.filter(user=request.user, payment_date__range=(month_start, month_end))
    
    context = {'fixed_expenses': fixed_expenses}
    return render(request, 'accountbook/current_month_fixed_expenses.html', context)

@login_required
def monthly_fixed_expenses(request):
    now = timezone.now()
    expenses = FixedExpense.objects.filter(user=request.user, payment_date__year=now.year, payment_date__month=now.month)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'accountbook/monthly_fixed_expenses.html', {'expenses': expenses, 'total_expenses': total_expenses})

@login_required
def income_summary_view(request):
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    
    # 当月の開始と終了の日時を計算
    current_month_start = datetime.datetime(current_year, current_month, 1, tzinfo=pytz.UTC)
    if current_month == 12:
        current_month_end = datetime.datetime(current_year + 1, 1, 1, tzinfo=pytz.UTC) - datetime.timedelta(seconds=1)
    else:
        current_month_end = datetime.datetime(current_year, current_month + 1, 1, tzinfo=pytz.UTC) - datetime.timedelta(seconds=1)

    monthly_fixed_expenses = FixedExpense.objects.filter(user=request.user, payment_date__year=current_year, payment_date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0
    monthly_expenses = VariableExpense.objects.filter(user=request.user, payment_date__year=current_year, payment_date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0
    
    # ここに収入の合計を計算するコードを追加
    total_income = AccountBook.objects.filter(user=request.user, record_date__year=current_year, record_date__month=current_month, type='income').aggregate(total=Sum('amount'))['total'] or 0

    # 月別の収入集計
    monthly_income = AccountBook.objects.filter(
        user=request.user,
        record_date__range=(current_month_start, current_month_end),
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # 年別の収入集計
    yearly_income = AccountBook.objects.filter(
        user=request.user,
        record_date__year=current_year,
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # 前月と前年の日付を計算
    previous_month = current_month - 1 if current_month > 1 else 12
    previous_year = current_year if current_month > 1 else current_year - 1
    previous_month_start = datetime.datetime(previous_year, previous_month, 1, tzinfo=pytz.UTC)
    previous_month_end = previous_month_start + datetime.timedelta(days=calendar.monthrange(previous_year, previous_month)[1]) - datetime.timedelta(seconds=1)

    # 前月の収入集計
    previous_month_income = AccountBook.objects.filter(
        user=request.user,
        record_date__range=(previous_month_start, previous_month_end),
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # 前年の収入集計
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
def update_income(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        income_id = data.get('id')
        field = data.get('field')
        value = data.get('value')
        
        if field == 'record_date':
            value = parse_date(value)

        # 収入データを更新
        income = AccountBook.objects.get(id=income_id)
        setattr(income, field, value)
        income.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

@login_required
@csrf_exempt
def delete_income(request, income_id):
    income = get_object_or_404(AccountBook, id=income_id, user=request.user)
    income.delete()
    return redirect('accountbook:income_list')

@login_required
def delete_variable_expense(request, expense_id):
    expense = get_object_or_404(VariableExpense, id=expense_id, user=request.user)
    expense.delete()
    return redirect('accountbook:variable_expense_list')

@login_required
def delete_fixed_expense(request, expense_id):
    expense = get_object_or_404(FixedExpense, id=expense_id, user=request.user)
    expense.delete()
    return redirect('accountbook:expense_list')

@csrf_exempt
def update_variable_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        expense_id = data.get('id')
        field = data.get('field')
        value = data.get('value')

        expense = VariableExpense.objects.get(id=expense_id)

        # amountフィールドの場合、値を整数に変換
        if field == 'amount':
            value = int(round(float(value)))

        setattr(expense, field, value)
        expense.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'}, status=400)
        
@csrf_exempt
def update_fixed_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        expense_id = data.get('id')
        field = data.get('field')
        value = data.get('value')

        expense = FixedExpense.objects.get(id=expense_id)

        # amountフィールドの場合、値を整数に変換
        if field == 'amount':
            value = int(round(float(value)))

        setattr(expense, field, value)
        expense.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

        
@require_POST
@csrf_exempt
def update_expense(request):
    try:
        data = json.loads(request.body)
        expense = Expense.objects.get(id=data['id'])
        setattr(expense, data['field'], data['value'])
        expense.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})