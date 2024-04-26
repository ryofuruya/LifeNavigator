from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm, ProfileForm, SignUpForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from .models import UserProfile

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

# ユーザー編集ビュー
class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    second_form_class = PasswordChangeForm
    template_name = 'accounts/edit_profile.html'

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
    success_url = '/registration/login/'  # 登録後のリダイレクト先

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
            return super(SignUpView, self).form_valid(form)
        else:
            return self.form_invalid(form)

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
