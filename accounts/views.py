from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm, ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
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


class UserEditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_edit.html'
    success_url = reverse_lazy('home')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:edit_profile')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()  # ユーザーを保存
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        # UserProfile を作成する前に、既に存在するかチェックする
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user)
        return super(SignUpView, self).form_valid(form)


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'registration/edit_profile.html', {'form': form})