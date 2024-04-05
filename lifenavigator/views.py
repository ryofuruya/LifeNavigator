from django.shortcuts import render, redirect
from accounts.models import UserProfile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'registration/profile.html', {'profile': profile})

def home(request):
    return render(request, 'home.html')

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

@login_required
def welcome(request):
    # ログインしていなければログインページにリダイレクト
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'welcome.html')