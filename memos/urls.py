from django.urls import path
from . import views

app_name = 'memos'

urlpatterns = [
    path('', views.memo_list, name='memo_list'),  # メモ一覧
    path('add/', views.memo_add, name='memo_add'),  # メモ追加
    path('<int:memo_id>/', views.memo_detail, name='memo_detail'),  # メモ詳細
    path('<int:memo_id>/edit/', views.memo_edit, name='memo_edit'),  # メモ編集
    path('<int:memo_id>/delete/', views.memo_delete, name='memo_delete'),  # メモ削除
]
