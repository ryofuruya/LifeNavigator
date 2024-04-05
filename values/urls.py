from django.urls import path
from .views import ValueListView, ValueDetailView, ValueCreateView, ValueUpdateView, ValueDeleteView
from . import views

app_name = 'values'

urlpatterns = [
    path('', views.ValueListView.as_view(), name='value-list'),
    path('<int:pk>/', views.ValueDetailView.as_view(), name='value-detail'),
    path('add/', views.ValueCreateView.as_view(), name='value-add'),
    path('<int:pk>/edit/', views.ValueUpdateView.as_view(), name='value-edit'),
    path('delete/<int:pk>/', views.ValueDeleteView.as_view(), name='value-delete'),
]
