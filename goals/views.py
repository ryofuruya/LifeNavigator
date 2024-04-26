from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal, Task
from .forms import GoalForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import Http404

@login_required
def goals_overview(request):
    # 目標設定の概要ページを表示
    return render(request, 'goals/goals_overview.html')

@login_required
def goal_setting(request):
    # 目標設定ページを表示
    return render(request, 'goals/goal_setting.html')

@login_required
def short_term_goals(request):
    # 短期目標に関連するタスクを表示
    tasks = Task.objects.filter(
        goal__user=request.user,
        goal__goal_type='short_term',
        completed=False
    ).order_by('deadline')
    return render(request, 'goals/short_term_goals.html', {'tasks': tasks})

@login_required
def medium_term_goals(request):
    # 中期目標に関連するタスクを表示
    tasks = Task.objects.filter(
        goal__user=request.user,
        goal__goal_type='medium_term',
        completed=False
    ).order_by('-deadline')
    return render(request, 'goals/medium_term_goals.html', {'tasks': tasks})

@login_required
def long_term_goals(request):
    # 長期目標に関連するタスクを表示
    tasks = Task.objects.filter(
        goal__user=request.user,
        goal__goal_type='long_term',
        completed=False
    ).order_by('-deadline')
    return render(request, 'goals/long_term_goals.html', {'tasks': tasks})

@login_required
def achieved_goals(request):
    # 完了したタスクを表示
    completed_tasks = Task.objects.filter(
        goal__user=request.user,
        completed=True
    ).order_by('-completed_at')
    return render(request, 'goals/achieved_goals.html', {'tasks': completed_tasks})

@login_required
def complete_task(request, task_id):
    # タスクを完了状態に更新
    task = get_object_or_404(Task, id=task_id, goal__user=request.user)
    task.completed = True
    task.completed_at = timezone.now()
    task.save()

    # タスクが関連する目標の種類に基づいて適切なページにリダイレクト
    if task.goal.goal_type == 'short_term':
        return redirect('goals:short_term_goals')
    elif task.goal.goal_type == 'medium_term':
        return redirect('goals:medium_term_goals')
    elif task.goal.goal_type == 'long_term':
        return redirect('goals:long_term_goals')
    else:
        return redirect('goals:goals_setting')  # 予期せぬケースのためのデフォルトのリダイレクト

@login_required
def task_detail(request, task_id):
    # タスクの詳細ページを表示
    task = get_object_or_404(Task, id=task_id, goal__user=request.user)
    context = {
        'task': task,
        'goal_type': task.goal.goal_type  # 仮定: Goalモデルにgoal_typeが存在する
    }
    return render(request, 'goals/task_detail.html', context)

@login_required
def task_edit(request, task_id):
    # 指定されたIDに基づいてタスクを取得し、ユーザーが所有していることを確認
    task = get_object_or_404(Task, id=task_id, goal__user=request.user)
    
    # POSTリクエストがある場合はフォームを処理
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            # タスクが関連する目標の種類に基づいて適切なページにリダイレクト
            if task.goal.goal_type == 'short_term':
                return redirect('goals:short_term_goals')
            elif task.goal.goal_type == 'medium_term':
                return redirect('goals:medium_term_goals')
            elif task.goal.goal_type == 'long_term':
                return redirect('goals:long_term_goals')
            else:
                return redirect('goals:goals_overview')
    else:
        # POSTリクエストがない場合は、既存のインスタンスでフォームを初期化
        form = TaskForm(instance=task)
    
    # フォームとタスクオブジェクトをテンプレートに渡す
    return render(request, 'goals/task_edit.html', {'form': form, 'task': task})

@login_required
def add_task_to_short_term_goal(request):
    # 短期目標へのタスク追加
    goal = Goal.objects.get_or_create(
        user=request.user,
        goal_type='short_term',
        defaults={
            'title': '短期目標のデフォルトタイトル',
            'description': '短期目標のデフォルト説明',
            'deadline': timezone.now() + timezone.timedelta(days=30),
            'completion_status': False,
            'achievement_percentage': 0,
        }
    )[0]  # get_or_create returns a tuple (object, created)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.goal = goal
            new_task.save()
            return redirect('goals:short_term_goals')
    else:
        form = TaskForm()
    return render(request, 'goals/add_task_to_short_term_goal.html', {'form': form})

@login_required
def add_task_to_medium_term_goal(request):
    # 中期目標へのタスク追加
    goal = Goal.objects.get_or_create(
        user=request.user,
        goal_type='medium_term',
        defaults={
            'title': '中期目標のデフォルトタイトル',
            'description': '中期目標のデフォルト説明',
            'deadline': timezone.now() + timezone.timedelta(days=180),
            'completion_status': False,
            'achievement_percentage': 0,
        }
    )[0]
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.goal = goal
            new_task.save()
            return redirect('goals:medium_term_goals')
    else:
        form = TaskForm()
    return render(request, 'goals/add_task_to_medium_term_goal.html', {'form': form})

@login_required
def add_task_to_long_term_goal(request):
    # 長期目標へのタスク追加
    goal = Goal.objects.get_or_create(
        user=request.user,
        goal_type='long_term',
        defaults={
            'title': '長期目標のデフォルトタイトル',
            'description': '長期目標のデフォルト説明',
            'deadline': timezone.now() + timezone.timedelta(days=365),
            'completion_status': False,
            'achievement_percentage': 0,
        }
    )[0]
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.goal = goal
            new_task.save()
            return redirect('goals:long_term_goals')
    else:
        form = TaskForm()
    return render(request, 'goals/add_task_to_long_term_goal.html', {'form': form})
