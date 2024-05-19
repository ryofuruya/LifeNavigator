from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm, ProfileForm, SignUpForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash, logout
from django.http import HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from accounts.models import UserProfile

# ユーザー詳細ビュー
@method_decorator(login_required, name='dispatch')
class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

# ユーザー削除ビュー
@method_decorator(login_required, name='dispatch')
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'common/delete_confirm.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('accounts:user_detail', kwargs={'pk': self.object.pk})
        return context

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

# ユーザー編集ビュー
class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    second_form_class = PasswordChangeForm
    template_name = 'accounts/edit_profile.html'

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if 'password_form' not in context:
                context['password_form'] = self.second_form_class(self.request.user)
            if self.request.POST:
                context['password_form'] = self.second_form_class(self.request.user, self.request.POST)
        return context
    
    def get_success_url(self):
        # 編集成功後にユーザー詳細ページにリダイレクト
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})

# ユーザー登録ビュー
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')  # 登録後のリダイレクト先

    def form_valid(self, form):
        # ユーザーオブジェクトを保存
        user = form.save()
        # ログイン処理
        login(self.request, user)
        # リダイレクト先を設定
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.object:
            return super().get_success_url()
        else:
            # フォールバックとしてホームへのURLを返す
            return reverse_lazy('home')

@login_required
def edit_profile(request):
    user_form = CustomUserChangeForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # パスワード変更後もセッション維持
            return redirect('accounts:user_detail', user.id)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })

class CustomLogoutView(View):
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        logout(request)
        return redirect('welcome')
