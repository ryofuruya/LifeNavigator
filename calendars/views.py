from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from .models import Event
from tasks.models import Task
from django.utils.timezone import now
from .forms import EventForm
from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def day_info(request, year, month, day):
    date = datetime.date(year, month, day)
    events = Event.objects.filter(date=date)  # その日のイベントを取得
    tasks = Task.objects.filter(deadline=date)  # 'date' を 'deadline' に変更
    context = {
        'events': events,
        'tasks': tasks,
    }
    return render(request, 'calendars/day_info.html', context)

@login_required
def calendar_view(request):
    today = now()
    current_year = today.year
    current_month = today.month

    events = Event.objects.filter(date__year=current_year, date__month=current_month)
    tasks = Task.objects.filter(deadline__year=current_year, deadline__month=current_month)

    event_days = [event.date.day for event in events]
    task_days = [task.deadline.day for task in tasks]

    context = {
        'event_days': json.dumps(event_days, cls=DjangoJSONEncoder),
        'task_days': json.dumps(task_days, cls=DjangoJSONEncoder),
        'current_year': current_year,
        'current_month': current_month
    }
    return render(request, 'calendars/calendar_view.html', context)

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'calendars/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'calendars/event_detail.html', {'event': event})

def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendars:event_list')  # 名前空間を使用してリダイレクト
    else:
        form = EventForm()
    return render(request, 'calendars/event_create.html', {'form': form})


def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)  # イベントのインスタンスを取得
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendars:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'calendars/event_edit.html', {'event': event, 'form': form})

def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('calendars:event_list')