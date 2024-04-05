from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import home, about, profile, edit_profile, welcome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goals/', include('goals.urls')),
    path('accountbook/', include('accountbook.urls', namespace='accountbook')),
    path('memos/', include('memos.urls', namespace='memos')),
    path('tasks/', include('tasks.urls')),
    path('', include('accounts.urls')),
    path('', views.home, name='home'),
    path('about/', about, name='about'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('welcome/', welcome, name='welcome'),
    path('calendars/', include('calendars.urls')), 
    path('values/', include('values.urls', namespace='values')), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
