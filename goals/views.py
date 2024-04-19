from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal, Task
from .forms import GoalForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST


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
    tasks = Task.objects.filter(
        goal__user=request.user,
        goal__goal_type='short_term',
        completed=False  # `status='in_progress'`の代わりに`completed=False`を使用
    ).order_by('deadline')
    return render(request, 'goals/short_term_goals.html', {'tasks': tasks})



@login_required
def medium_term_goals(request):
    tasks = Task.objects.filter(goal__user=request.user, goal__goal_type='medium_term', completed=False).order_by('-deadline')
    return render(request, 'goals/medium_term_goals.html', {'tasks': tasks})

@login_required
def long_term_goals(request):
    tasks = Task.objects.filter(goal__user=request.user, goal__goal_type='long_term', completed=False).order_by('-deadline')
    return render(request, 'goals/long_term_goals.html', {'tasks': tasks})

@login_required
def add_task_to_short_term_goal(request):

    goal, created = Goal.objects.get_or_create(
        user=request.user,
        goal_type='short_term',
        defaults={
            'title': '短期目標のデフォルトタイトル',
            'description': '短期目標のデフォルト説明',
            'deadline': timezone.now() + timezone.timedelta(days=30),  # 例えば30日後をデフォルトの期限とする
            'completion_status': False,
            'achievement_percentage': 0,
        }
    )
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.goal = goal
            new_task.save()
            return redirect('goals:short_term_goals')
    else:
        form = TaskForm()
    return render(request, 'goals/add_task_to_short_term_goal.html', {'form': form})



@login_required
def add_task_to_medium_term_goal(request):
    # 中期目標を取得するか、存在しない場合は作成します。
    goal, created = Goal.objects.get_or_create(
        user=request.user,
        goal_type='medium_term',
        defaults={
            'title': '中期目標のデフォルトタイトル',
            'description': '中期目標のデフォルト説明',
            'deadline': timezone.now() + timezone.timedelta(days=30),  # 例えば30日後をデフォルトの期限とする
            'completion_status': False,
            'achievement_percentage': 0,
        }
    )
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.goal = goal
            new_task.save()
            return redirect('goals:medium_term_goals')
    else:
        form = TaskForm()
    return render(request, 'goals/add_task_to_medium_term_goal.html', {'form': form})

@login_required
def add_task_to_long_term_goal(request):
    # 長期目標を取得するか、存在しない場合は作成します。
    goal, created = Goal.objects.get_or_create(
        user=request.user,
        goal_type='long_term',
        defaults={
            'title': '長期目標のデフォルトタイトル',
            'description': '長期目標のデフォルト説明',
            'deadline': timezone.now() + timezone.timedelta(days=365),  # 例えば365日後をデフォルトの期限とする
            'completion_status': False,
            'achievement_percentage': 0,
        }
    )
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.goal = goal
            new_task.save()
            return redirect('goals:long_term_goals')
    else:
        form = TaskForm()
    return render(request, 'goals/add_task_to_long_term_goal.html', {'form': form})


@login_required
def achieved_goals(request):
    # 完了したタスクを取得
    completed_tasks = Task.objects.filter(goal__user=request.user, completed=True).order_by('-completed_at')
    return render(request, 'goals/achieved_goals.html', {'tasks': completed_tasks})

    
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('goals:short_term_goals')

@login_required
def task_detail(request, task_id):
    # `user=request.user` を `goal__user=request.user` に変更しています
    task = get_object_or_404(Task, id=task_id, goal__user=request.user)
    return render(request, 'goals/task_detail.html', {'task': task})


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, goal__user=request.user)  # `goal__user`を使用してユーザーを絞り込む
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            # 編集後の遷移先を変更する
            return redirect(request.POST.get('next', 'goals:goals_overview'))
    else:
        form = TaskForm(instance=task)
    return render(request, 'goals/task_edit.html', {'form': form, 'task': task})

@login_required
@require_POST
def task_complete(request):
    task_ids = request.POST.getlist('task_id')
    Task.objects.filter(id__in=task_ids, goal__user=request.user).update(completed=True, completed_at=timezone.now())

    # 遷移先のURLを動的に決定するためのパラメータを取得
    redirect_page = request.POST.get('redirect_page')
    if redirect_page == 'short_term':
        return redirect('goals:short_term_goals')
    elif redirect_page == 'medium_term':
        return redirect('goals:medium_term_goals')
    elif redirect_page == 'long_term':
        return redirect('goals:long_term_goals')
    elif redirect_page == 'achieved':
        return redirect('goals:achieved_goals')  # 完了したタスクのページにリダイレクト
    else:
        return redirect('goals:goals_overview')  # その他のケースでは目標概要ページにリダイレクト
