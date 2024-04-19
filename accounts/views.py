from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm, ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
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
        if 'password_form' not in context:
            context['password_form'] = self.second_form_class(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        password_form = self.second_form_class(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            return self.form_valid(form, password_form)
        else:
            return self.form_invalid(form, password_form)

    def form_valid(self, form, password_form):
        form.save()
        password_form.save()
        update_session_auth_hash(self.request, password_form.user)  # Important!
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, password_form):
        return self.render_to_response(self.get_context_data(form=form, password_form=password_form))

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})

# ユーザー登録ビュー
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:edit_profile')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user)
        return super(SignUpView, self).form_valid(form)

@login_required
def edit_profile(request):
    user = request.user
    profile_form = ProfileForm(instance=user.profile)
    password_form = PasswordChangeForm(user)
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=user.profile)
            if profile_form.is_valid():
                profile_form.save()
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
    return render(request, 'registration/edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
