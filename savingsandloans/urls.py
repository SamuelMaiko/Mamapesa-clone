from django.urls import path
from .views import LoanRequestView, LoanRepaymentView

urlpatterns = [   
    path('loans/', LoanRequestView.as_view(), name='loans'),
    path('repayments/', LoanRepaymentView.as_view(), name='repayments'),
]
