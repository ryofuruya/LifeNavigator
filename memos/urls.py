from django.urls import path
from . import views

app_name = 'memos'

urlpatterns = [
    path('list/', views.memo_list, name='memo_list'),
    path('add/', views.memo_add, name='memo_add'),
    path('<int:pk>/edit/', views.memo_edit, name='memo_edit'),
    path('<int:pk>/delete/', views.memo_delete, name='memo_delete'),
    path('<int:pk>/', views.memo_detail, name='memo_detail'),
]
