from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from .models import Event  # 適切なパスを確認

@login_required
def day_info(request, year, month, day):
    date = datetime.date(year, month, day)
    events = Event.objects.filter(date=date)  # その日のEventデータを取得
    context = {
        'events': events,
    }
    return render(request, 'calendars/day_info.html', context)  # 実際に存在するテンプレート名に置き換える

def calendar_view(request):
    # ここにカレンダー表示に関するロジックを実装
    return render(request, 'calendars/calendar_view.html')
