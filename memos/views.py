from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo
from .forms import MemoSearchForm, MemoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.timezone import localtime

@login_required
def memo_list(request):
    form = MemoSearchForm(request.GET or None)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        memos = Memo.objects.filter(user=request.user)
        
        if keyword:
            memos = memos.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
        
        if start_date:
            memos = memos.filter(created_at__date__gte=start_date)  # created を created_at に修正
        
        if end_date:
            memos = memos.filter(created_at__date__lte=end_date)  # created を created_at に修正

    else:
        memos = Memo.objects.filter(user=request.user)

    return render(request, 'memos/memo_list.html', {'form': form, 'memos': memos})

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
def memo_edit(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memos:memo_list')
    else:
        form = MemoForm(instance=memo)
    return render(request, 'memos/memo_edit.html', {'form': form})

@login_required
def memo_delete(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == 'POST':
        memo.delete()
        return redirect('memos:memo_list')
    return render(request, 'memos/memo_delete.html', {'memo': memo})

@login_required
def memo_detail(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    return render(request, 'memos/memo_detail.html', {'memo': memo})
