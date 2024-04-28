from django.contrib import admin
from django.urls import path, include
from . import views
from accounts.views import SignUpView, CustomLogoutView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goals/', include('goals.urls')),
    path('accountbook/', include('accountbook.urls', namespace='accountbook')),
    path('memos/', include('memos.urls', namespace='memos')),
    path('tasks/', include('tasks.urls')),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('calendars/', include('calendars.urls')),
    path('values/', include('values.urls', namespace='values')),
    # Djangoの認証システムに関連するURLを含める
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('welcome/', views.welcome, name='welcome'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('registration/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
