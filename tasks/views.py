from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, TaskFormSet, CompletedTaskFilterForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import localdate
from django.forms import modelformset_factory
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
import datetime
from django.db.models import Q

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).exclude(status='completed').order_by('priority')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def daily_tasks(request):
    if request.method == 'POST':
        formset = TaskFormSet(queryset=Task.objects.filter(user=request.user, deadline=localdate(), status='in_progress', task_type='daily').order_by('priority'))
        if formset.is_valid():
            formset.save()
            return redirect('tasks:daily_tasks')
    else:
        formset = TaskFormSet(queryset=Task.objects.filter(user=request.user, deadline=localdate(), status='in_progress').order_by('priority'))
    return render(request, 'tasks/daily_tasks.html', {'formset': formset})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:daily_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task})

@login_required
def add_daily_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.deadline = timezone.localdate()  # 'today' の代わりに 'localdate()' を使用
            new_task.status = 'in_progress'  # 新しいタスクのステータスを設定
            new_task = form.save()
            new_task.task_type = 'daily'
            return redirect('tasks:daily_tasks')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_daily_task.html', {'form': form})

@login_required
def add_monthly_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            today = timezone.now().date()
            new_task.deadline = today.replace(day=1)  # 月の初日をdeadlineとして設定
            new_task.status = 'in_progress'
            new_task.task_type = 'monthly'
            new_task = form.save()
            return redirect('tasks:monthly_tasks')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_monthly_task.html', {'form': form})


@login_required
def monthly_tasks(request):
    today = timezone.now()
    year = today.year
    month = today.month
    tasks = Task.objects.filter(
        user=request.user,
        deadline__year=year,
        deadline__month=month,
        status='in_progress',
        task_type='monthly'
    ).order_by('priority')
    return render(request, 'tasks/monthly_tasks.html', {'tasks': tasks})

@require_POST
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if task.status != 'completed':  # タスクがまだ完了していない場合のみ更新
        task.status = 'completed'
        task.completed_at = timezone.now()  # 完了日時を現在の日時で更新
        task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def completed_tasks(request):
    form = CompletedTaskFilterForm(request.GET)
    completed_tasks_query = Task.objects.filter(user=request.user, status='completed')

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        completed_date = form.cleaned_data.get('completed_date')

        if keyword:
            completed_tasks_query = completed_tasks_query.filter(title__icontains=keyword)

        if completed_date:
            # completed_at の日付部分でフィルタリング
            completed_tasks_query = completed_tasks_query.filter(completed_at__date=completed_date)

    completed_tasks = completed_tasks_query.order_by('-completed_at')
    return render(request, 'tasks/completed_tasks.html', {'completed_tasks': completed_tasks, 'form': form})