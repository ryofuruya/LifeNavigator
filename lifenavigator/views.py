from django.shortcuts import render, redirect
from accounts.models import UserProfile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'registration/profile.html', {'profile': profile})

def home(request):
    if request.user.is_authenticated:
        # ログインしている場合はホームページを表示
        return render(request, 'home.html')
    else:
        # ログインしていない場合はサインアップページにリダイレクト
        return redirect('accounts:signup')

def about(request):
    return render(request, 'about.html')

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
