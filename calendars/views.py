from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from .models import Event
from tasks.models import Task
from django.utils.timezone import now
from .forms import EventForm
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.urls import reverse

@login_required
def day_info(request, year, month, day):
    # 引数を整数に変換
    year = int(year)
    month = int(month)
    day = int(day)
    # 正しい日付オブジェクトを作成
    date = datetime.date(year, month, day)
    events = Event.objects.filter(date=date, is_deleted=False, user=request.user)  # ログインユーザーのイベントのみ取得
    tasks = Task.objects.filter(deadline=date, is_deleted=False, user=request.user)  # ログインユーザーのタスクのみ取得
    context = {
        'events': events,
        'tasks': tasks,
    }
    return render(request, 'calendars/day_info.html', context)

@login_required
def calendar_view(request):
    user = request.user
    current_month = now().month
    current_year = now().year

    events = Event.objects.filter(is_deleted=False, user=user)
    tasks = Task.objects.filter(is_deleted=False, user=user)

    event_days = {}
    task_days = {}

    for event in events:
        event_date = event.date
        year = event_date.year
        month = event_date.month
        day = event_date.day
        if year not in event_days:
            event_days[year] = {}
        if month not in event_days[year]:
            event_days[year][month] = []
        event_days[year][month].append(day)

    for task in tasks:
        task_date = task.deadline
        year = task_date.year
        month = task_date.month
        day = task_date.day
        if year not in task_days:
            task_days[year] = {}
        if month not in task_days[year]:
            task_days[year][month] = []
        task_days[year][month].append(day)

    context = {
        'event_days': json.dumps(event_days, cls=DjangoJSONEncoder),
        'task_days': json.dumps(task_days, cls=DjangoJSONEncoder),
    }
    return render(request, 'calendars/calendar_view.html', context)

@login_required
def event_list(request):
    events = Event.objects.filter(is_deleted=False, user=request.user).order_by('date')  # ログインユーザーのイベントのみ取得
    return render(request, 'calendars/event_list.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    return render(request, 'calendars/event_detail.html', {'event': event})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('calendars:event_list')  # 名前空間を使用してリダイレクト
    else:
        form = EventForm()
    return render(request, 'calendars/event_create.html', {'form': form})

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)  # ログインユーザーのイベントのみ取得
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendars:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'calendars/event_edit.html', {'event': event, 'form': form})

@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('calendars:event_list')
    return render(request, 'common/delete_confirm.html', {'object': event, 'cancel_url': reverse('calendars:event_detail', kwargs={'event_id': event_id})})
