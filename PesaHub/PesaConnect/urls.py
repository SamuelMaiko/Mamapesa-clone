from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('custom-users/', views.custom_user_list_create, name='custom-user-list-create'),
    path('trust-scores/', views.trust_score_list_create, name='trust-score-list-create'),
    path('savings/', views.savings_item_list_create, name='savings-list-create'),
    path('loans/', views.loan_item_list_create, name='loan-list-create'),
    path('items/', views.item_list_create, name='item-list-create'),
    path('loan-items/', views.loan_item_list_create, name='loan-item-list-create'),
    path('transactions/', views.transaction_list_create, name='transaction-list-create'),
    path('savings-items/', views.savings_item_list_create, name='savings-item-list-create'),
    path('withdrawals/', views.withdrawal_list_create, name='withdrawal-list-create'),
    path('user-details/', views.user_details_list_create, name='user-details-list-create'),
    path('savings-payments/', views.savings_item_list_create, name='savings-payment-list-create'),
]
