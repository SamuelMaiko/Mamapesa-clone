# serializers.py
from rest_framework import serializers
from newmamapesa.models import Loan, LoanRepayment
from django.utils import timezone
from decimal import Decimal

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['amount', 'purpose']

    def create(self, validated_data):
        user = self.context['request'].user  
        amount_requested = Decimal(validated_data['amount'])      
       
        if user.loan_limit >= amount_requested:
            interest_rate = user.interest_rate
            total_loan_amount = amount_requested * (1 + interest_rate / 100)

            loan = Loan(
                user=user,
                amount=total_loan_amount,
                interest_rate=interest_rate,
                duration_months=3, 
                application_date=timezone.now().date(),
                is_approved=True,
                is_active=True,
                disbursed=True,
                purpose=validated_data['purpose'],
                due_date=timezone.now().date() + timedelta(days=90)  # Set your desired due date
            )

            loan.save()
            
            user.loan_limit -= total_loan_amount
            user.save()

            print(f"Loan limit after request: {user.loan_limit}")

            return loan
        else:
            print(f"Insufficient loan limit. User's loan limit: {user.loan_limit}, Amount requested: {amount_requested}")
            raise serializers.ValidationError({'error': 'Insufficient loan limit'})


class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = ['amount_paid']

    def create(self, validated_data):
        user = self.context['request'].user
        loan = user.loans.filter(is_active=True, disbursed=True).first()

        if not loan:
            raise serializers.ValidationError({'error': 'No active loan found for the user'})

        amount_paid = validated_data['amount_paid']  # Correct field name

        remaining_loan_amount = loan.calculate_remaining_amount()

        if amount_paid > remaining_loan_amount:
            # Save the excess amount to the user's savings
            excess_amount = amount_paid - remaining_loan_amount

            # Assuming you have a Savings model
            savings = user.savings.create(
                amount_saved=excess_amount,
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timezone.timedelta(days=90),
                purpose="Excess loan payment savings"
            )

            amount_paid = remaining_loan_amount  # Set amount_paid to the remaining loan amount

        loan_repayment = LoanRepayment.objects.create(
            loan=loan,
            amount_paid=amount_paid
        )

        # Make repayment and handle loan status
        loan.make_repayment(amount_paid)

        return loan_repayment
class LoanSerializer(serializers.ModelSerializer):
    remaining_balance = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['amount', 'repaid_amount', 'total_paid', 'remaining_balance']

    def get_remaining_balance(self, obj):
        return obj.get_remaining_balance()