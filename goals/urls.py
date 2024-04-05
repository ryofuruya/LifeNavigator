from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goals_overview, name='goals_overview'),  # goals/ へのアクセスに対応
    path('goal_setting/', views.goal_setting, name='goal_setting'),
    path('short_term_goals/', views.short_term_goals, name='short_term_goals'),
    path('medium_term_goals/', views.medium_term_goals, name='medium_term_goals'),
    path('long_term_goals/', views.long_term_goals, name='long_term_goals'),
    path('achieved_goals/', views.achieved_goals, name='achieved_goals'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('add_task_to_short_term_goal/', views.add_task_to_short_term_goal, name='add_task_to_short_term_goal'),
    path('add_task_to_medium_term_goal/', views.add_task_to_medium_term_goal, name='add_task_to_medium_term_goal'),
    path('add_task_to_long_term_goal/', views.add_task_to_long_term_goal, name='add_task_to_long_term_goal'),
    path('task_edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('task_complete/', views.task_complete, name='task_complete'),
]
