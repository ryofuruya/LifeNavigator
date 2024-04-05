from django.urls import path
from . import views

app_name = 'calendars'

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),
    path('day-info/<int:year>/<int:month>/<int:day>/', views.day_info, name='day_info'),
]
