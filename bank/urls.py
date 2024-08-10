from django.urls import path
from . import views

urlpatterns = [
    path('accounts/account_list', views.account_list, name='account_list'),
    path('accounts/max_balance', views.max_balance, name='max_balance'),
    path('accounts/min_balances', views.min_balances, name='min_balances'),
    path('accounts/account_number_greater_balance', views.account_number_greater_balance, name='account_number_greater_balance'),
    path('accounts/id_greater_balance', views.id_greater_balance, name='id_greater_balance'),
    path('accounts/get_total_balance_of_user', views.get_total_balance_of_user, name='get_total_balance_of_user'),
    path('transfer-funds/', views.transfer_funds, name='transfer_funds'),
]
