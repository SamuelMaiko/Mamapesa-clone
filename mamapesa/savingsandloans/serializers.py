from rest_framework import serializers
from newmamapesa.models import Loan, LoanRepayment,Savings, SavingsItem,SavingsTransaction, Item, LoanTransaction, CustomUser
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

class SavingsAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Savings
        fields=["id","amount_saved","start_date"]

class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Item
        fields=["id","name","description"]

class SavingsItemSerializer(serializers.ModelSerializer):
    item=ItemSerializer()
    # start_date = serializers.DateField(format='%Y-%m-%d')
    # due_date = serializers.DateField(format='%Y-%m-%d')
    class Meta:
        model=SavingsItem
        # fields=["id","item","amount_saved","target_amount","start_date","remaining_amount","daily_payment","remaining_days", "due_date","achieved","in_progress"]
        fields=["id","item","amount_saved","target_amount","start_date","remaining_amount","installment","days_payment","remaining_days", "due_date","saving_period","is_achieved","in_progress"]
        
# class SavingsItemSerializer2(serializers.ModelSerializer):
#     item=ItemSerializer()
#     # start_date = serializers.DateField(format='%Y-%m-%d')
#     # due_date = serializers.DateField(format='%Y-%m-%d')
#     class Meta:
#         model=SavingsItem
#         # fields=["id","item","amount_saved","target_amount","start_date","remaining_amount","daily_payment","remaining_days", "due_date","achieved","in_progress"]
#         fields=["id","item","amount_saved","target_amount","start_date","end_date"]

class SavingsTransactionSerializer(serializers.ModelSerializer):
    # item=
    class Meta:
        model=SavingsTransaction
        fields=["id", "type", "amount","timestamp"]
        
class LoanRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ['amount', 'purpose']

class LoanRepaymentSerializer(serializers.ModelSerializer):
    amount_paid = serializers.IntegerField()
    class Meta:
        model = LoanRepayment
        fields = ['amount_paid']

class LoanTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanTransaction
        fields = '__all__'
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print(f"User: {self.request.user.username}")
        print(response.data) 
        return response

        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['loan_owed', 'loan_limit']


    
