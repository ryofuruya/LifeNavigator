from django.urls import path
from . import views

app_name = 'calendars'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('day-info/<int:year>/<int:month>/<int:day>/', views.day_info, name='day_info'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/edit/<int:event_id>/', views.event_edit, name='event_edit'),
    path('events/delete/<int:event_id>/', views.event_delete, name='event_delete'),
]
