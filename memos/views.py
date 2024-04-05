from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo
from .forms import MemoSearchForm, MemoForm
from django.contrib.auth.decorators import login_required

@login_required
def memo_list(request):
    form = MemoSearchForm(request.GET or None)
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword', '')
        memos = Memo.objects.filter(user=request.user, content__icontains=keyword)
    else:
        memos = Memo.objects.filter(user=request.user)
    return render(request, 'memos/memo_list.html', {'memos': memos, 'form': form})

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
