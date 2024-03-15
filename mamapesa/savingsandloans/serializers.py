from rest_framework import serializers
# from newmamapesa.models import Loan,Savings, SavingsItem,SavingsTransaction, Item, LoanTransaction, CustomUser
from newmamapesa.models import Loan,Savings, SavingsItem, Item, CustomUser, Payment

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
    class Meta:
        model=SavingsItem
        fields=["id","item","amount_saved","target_amount","start_date","remaining_amount","installment","days_payment","remaining_days", "due_date","saving_period","is_achieved","in_progress"]

class PaymentSerializer(serializers.ModelSerializer):
    payment_name=serializers.SerializerMethodField()
    is_addition=serializers.SerializerMethodField()
    class Meta:
        model=Payment
        fields=['amount', 'type', 'payment_name','status', 'payment_date', 'is_addition']

    def get_payment_name(self, obj):
        return obj.payment_method.name
    
    def get_is_addition(self, obj):
        if obj.type=="Loan Disbursement" or obj.type=="Savings Deposit":
            return True
        return False
        
# class SavingsTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=SavingsTransaction
#         fields=["id", "type", "amount","timestamp"]
class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['amount']
# class LoanTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LoanTransaction
#         fields = '__all__'
    
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         print(f"User: {self.request.user.username}")
#         print(response.data) 
#         return response
class CustomUserSerializer(serializers.ModelSerializer):
    remaining_days = serializers.SerializerMethodField()
    class Meta:
        model = Loan
        fields = ['id', 'amount', 'repaid_amount', 'default_days', 'remaining_days', 'application_date', 'due_date']

    def get_remaining_days(self, obj):
        return obj.calculated_remaining_days