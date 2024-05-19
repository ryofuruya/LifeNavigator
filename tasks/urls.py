from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('daily_tasks/', views.daily_tasks, name='daily_tasks'),
    path('daily/<int:pk>/', views.daily_task_detail, name='daily_task_detail'),
    path('daily/<int:pk>/edit/', views.daily_task_edit, name='daily_task_edit'),
    path('daily/<int:pk>/delete/', views.daily_task_delete, name='daily_task_delete'),  # daily_task_deleteを追加
    path('daily/<int:pk>/complete_confirm/', views.complete_confirm, name='daily_task_complete_confirm'),
    path('add/daily/', views.add_daily_task, name='add_daily_task'),
    path('monthly_tasks/', views.monthly_tasks, name='monthly_tasks'),
    path('<int:pk>/monthly_detail/', views.monthly_task_detail, name='monthly_task_detail'), 
    path('monthly/<int:pk>/edit/', views.monthly_task_edit, name='monthly_task_edit'),
    path('monthly/<int:pk>/delete/', views.monthly_task_delete, name='monthly_task_delete'),  # monthly_task_deleteを追加
    path('monthly/<int:pk>/complete_confirm/', views.complete_confirm, name='monthly_task_complete_confirm'),
    path('add/monthly/', views.add_monthly_task, name='add_monthly_task'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('task/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),
]
