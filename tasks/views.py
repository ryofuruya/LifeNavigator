from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, TaskFormSet, CompletedTaskFilterForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import localdate
from django.forms import modelformset_factory
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse, HttpResponse
import json
import logging


logger = logging.getLogger(__name__)

@login_required
def task_list(request):
    """Display a list of all incomplete tasks for the user."""
    tasks = Task.objects.filter(user=request.user).exclude(status='completed').order_by('priority')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def daily_tasks(request):
    """Manage daily tasks for the user."""
    # 現在日付とタスクタイプが 'daily' であり、さらにステータスが 'completed' でないタスクを取得
    tasks = Task.objects.filter(
        user=request.user, 
        deadline=localdate(), 
        task_type='daily'
    ).exclude(status='completed').order_by('priority')
    return render(request, 'tasks/daily_tasks.html', {'tasks': tasks})

@login_required
def daily_task_detail(request, pk):
    """Display details for a specific daily task."""
    task = get_object_or_404(Task, pk=pk, user=request.user, task_type='daily')
    return render(request, 'tasks/daily_task_detail.html', {'task': task})

@login_required
def daily_task_edit(request, pk):
    """Edit a specific daily task."""
    task = get_object_or_404(Task, pk=pk, user=request.user, task_type='daily')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:daily_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/daily_task_edit.html', {'form': form, 'task': task})

@login_required
def monthly_tasks(request):
    """Display a list of monthly tasks that are not completed."""
    current_month = timezone.now().month
    current_year = timezone.now().year
    tasks = Task.objects.filter(
        user=request.user,
        task_type='monthly',
        deadline__year=current_year,
        deadline__month=current_month
    ).exclude(status='completed').order_by('priority')
    return render(request, 'tasks/monthly_tasks.html', {'tasks': tasks})

@login_required
def monthly_task_detail(request, pk):
    """Display details for a specific monthly task."""
    task = get_object_or_404(Task, pk=pk, user=request.user, task_type='monthly')
    return render(request, 'tasks/monthly_task_detail.html', {'task': task})

@login_required
def monthly_task_edit(request, pk):
    """Edit a specific monthly task."""
    task = get_object_or_404(Task, pk=pk, user=request.user, task_type='monthly')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:monthly_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/monthly_task_edit.html', {'form': form, 'task': task})

@login_required
def add_daily_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.deadline = form.cleaned_data['deadline']  # フォームから日付を取得
            new_task.task_type = 'daily'
            new_task.save()
            return redirect('tasks:daily_tasks')
        else:
            logger.error(f"Form errors: {form.errors}")  # エラーをログに記録
    else:
        form = TaskForm()
    return render(request, 'tasks/add_daily_task.html', {'form': form})

@login_required
def add_monthly_task(request):
    """Add a new monthly task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.deadline = form.cleaned_data['deadline']  # フォームから日付を取得
            new_task.status = 'in_progress'
            new_task.task_type = 'monthly'
            new_task.save()
            return redirect('tasks:monthly_tasks')
        else:
            return render(request, 'tasks/add_monthly_task.html', {'form': form})
    else:
        form = TaskForm()
        return render(request, 'tasks/add_monthly_task.html', {'form': form})

@login_required
@require_POST
def update_task_status(request, task_id):
    """Update the status of a task to 'completed' and record the completion time."""
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if task.status != 'completed':
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        
    # Redirect to the appropriate task page based on the task type
    if task.task_type == 'daily':
        return redirect('tasks:daily_tasks')
    elif task.task_type == 'monthly':
        return redirect('tasks:monthly_tasks')
    else:
        # Default redirect if task type is neither daily nor monthly
        return redirect('tasks:task_list')

@login_required
def completed_tasks(request):
    """Display completed tasks."""
    completed_tasks = Task.objects.filter(user=request.user, status='completed').order_by('-completed_at')
    return render(request, 'tasks/completed_tasks.html', {'completed_tasks': completed_tasks})

