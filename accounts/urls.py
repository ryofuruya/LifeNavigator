from django.urls import path
from .views import UserDetailView, UserDeleteView, UserEditView
from . import views


app_name = 'accounts' 

urlpatterns = [
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/edit/', UserEditView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
