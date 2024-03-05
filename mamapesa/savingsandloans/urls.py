from django.urls import path, include
from . import views

urlpatterns=[
    path("savings-account/", views.SavingsAccountView.as_view(), name="savings-account"),
    path("savings-items/", views.SavingsItemsView.as_view(), name="savings-items"),
    path("savings-items/<int:id>", views.SavingsItemView.as_view(), name="savings-item"),
    path("deposit-savings/<int:saving_item_id>", views.DepositSavingsView.as_view(), name="deposit-savings"),
    # path("withdraw-savings/<int:saving_item_id>", views.WithdrawSavingsView.as_view(), name="withdraw-savings"),
    # path("suspend-savings-items/<int:saving_item_id>", views.SuspendSavingsItemView.as_view(), name="suspend-savings-items"),
    path("create-saving/", views.CreateSavingsView.as_view(), name="create-savings"),
    path("change-saving-period/<int:saving_item_id>", views.ChangeSavingsPeriodView.as_view(), name="change-savings-period"),
    # path('loans/', views.LoanRequestView.as_view(), name='loans'),
    # path('repayments/', views.LoanRepaymentView.as_view(), name='repayments'),
]
