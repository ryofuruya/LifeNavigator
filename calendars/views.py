from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from .models import Event
from tasks.models import Task

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

def calendar_view(request):
    # ここにカレンダー表示に関するロジックを実装
    return render(request, 'calendars/calendar_view.html')
