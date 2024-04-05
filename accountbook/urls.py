from django.urls import path
from . import views
from .views import accountbook_list, add_account_entry, summary_view,income_list, variable_expense_list, expense_list, delete_income

app_name = 'accountbook' 

urlpatterns = [
    path('', accountbook_list, name='accountbook_list'),
    path('add/', add_account_entry, name='add_account_entry'),
    path('add_fixed_expense/', views.add_fixed_expense, name='add_fixed_expense'),
    path('add_variable_expense/', views.add_variable_expense, name='add_variable_expense'),
    path('summary/', views.summary_view, name='summary_view'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('incomes/', income_list, name='income_list'),
    path('variable_expenses/', variable_expense_list, name='variable_expense_list'),
    path('expenses/', expense_list, name='expense_list'),
    path('monthly-fixed-expenses/', views.monthly_fixed_expenses, name='monthly_fixed_expenses'),
    path('income_summary/', views.income_summary_view, name='income_summary_view'),
    path('update_income/', views.update_income, name='update_income'),
    path('delete_income/<int:income_id>/', delete_income, name='delete_income'),
    path('delete_variable_expense/<int:expense_id>/', views.delete_variable_expense, name='delete_variable_expense'),
    path('delete_fixed_expense/<int:expense_id>/', views.delete_fixed_expense, name='delete_fixed_expense'),
    path('update_variable_expense/', views.update_variable_expense, name='update_variable_expense'),
    path('update_fixed_expense/', views.update_fixed_expense, name='update_fixed_expense'), # type: ignore
]
