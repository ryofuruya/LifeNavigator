from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('daily/', views.daily_tasks, name='daily_tasks'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('monthly/', views.monthly_tasks, name='monthly_tasks'),
    path('add/daily/', views.add_daily_task, name='add_daily_task'),
    path('add/monthly/', views.add_monthly_task, name='add_monthly_task'),
    path('task/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
]

