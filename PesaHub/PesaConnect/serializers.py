
"""
Serializers for Mamapesa-backend API

These serializers convert Django models into JSON format and vice versa for API endpoints.

Usage:
    These serializers are used within Django REST Framework to handle serialization and deserialization of Django model instances.

Overview:
    - CustomUserSerializer: Serializer for the CustomUser model.
    - TrustScoreSerializer: Serializer for the TrustScore model.
    - SavingsSerializer: Serializer for the Savings model.
    - LoanSerializer: Serializer for the Loan model.
    - ItemSerializer: Serializer for the Item model.
    - LoanItemSerializer: Serializer for the LoanItem model.
    - TransactionSerializer: Serializer for the Transaction model.
    - SavingsItemSerializer: Serializer for the SavingsItem model.
    - WithdrawalSerializer: Serializer for the Withdrawal model.
    - UserDetailsSerializer: Serializer for the UserDetails model.
    - SavingsPaymentSerializer: Serializer for the SavingsPayment model.

Each serializer defines a Meta class specifying the corresponding model and the fields to be included in the serialization process.

"""
from rest_framework import serializers
from .models import CustomUser, TrustScore, Savings, Loan, Item, LoanItem, Transaction, SavingsItem, Withdrawal, UserDetails, SavingsPayment
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class TrustScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustScore
        fields = '__all__'

class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class LoanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanItem
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class SavingsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsItem
        fields = '__all__'
class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class SavingsPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsPayment
        fields = '__all__'
