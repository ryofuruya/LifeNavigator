from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# ユーザー詳細ビュー
@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'


# ユーザー削除ビュー
@method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('home')


class UserEditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_edit.html'
    success_url = reverse_lazy('home')