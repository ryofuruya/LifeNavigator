from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo
from .forms import MemoSearchForm, MemoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Min, Max
from django.utils.timezone import localtime
from django.urls import reverse

@login_required
def memo_list(request):
    memos = Memo.objects.filter(user=request.user)

    # 最も古い日付と新しい日付を取得
    date_range = memos.aggregate(oldest_date=Min('created_at'), newest_date=Max('created_at'))
    oldest_date = date_range['oldest_date']
    newest_date = date_range['newest_date']

    if request.method == 'GET' and not request.GET:
        initial_data = {
            'start_date': oldest_date,
            'end_date': newest_date,
        }
        form = MemoSearchForm(initial=initial_data)
    else:
        form = MemoSearchForm(request.GET)

    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if keyword:
            memos = memos.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
        
        if start_date:
            memos = memos.filter(created_at__date__gte=start_date)
        
        if end_date:
            memos = memos.filter(created_at__date__lte=end_date)

    return render(request, 'memos/memo_list.html', {'form': form, 'memos': memos, 'oldest_date': oldest_date, 'newest_date': newest_date})

@login_required
def memo_add(request):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = request.user
            memo.save()
            return redirect('memos:memo_list')
    else:
        form = MemoForm()
    return render(request, 'memos/memo_add.html', {'form': form})

@login_required
def memo_edit(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)
    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memos:memo_list')
    else:
        form = MemoForm(instance=memo)
    return render(request, 'memos/memo_edit.html', {'form': form})

@login_required
def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)
    return render(request, 'memos/memo_detail.html', {'memo': memo})

@login_required
def memo_delete(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)
    if request.method == 'POST':
        memo.delete()
        return redirect('memos:memo_list')  # メモ一覧ページにリダイレクト
    return render(request, 'common/delete_confirm.html', {'object': memo, 'cancel_url': reverse('memos:memo_detail', kwargs={'memo_id': memo.id})})
