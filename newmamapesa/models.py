from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from decimal import Decimal

class CustomUser(AbstractUser):
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    idnumber = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email=models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    loan_limit = models.DecimalField(max_digits=10, decimal_places=2, default=8000)  # Add loan_limit field
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)  # Add interest_rate field
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    def save(self, *args, **kwargs):
       
        if self.loan_limit is None or self.loan_limit == 0:
            self.loan_limit = 8000
        super().save(*args, **kwargs)

    def __str__(self):

        return self.username
    
class TrustScore(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='their_trust_score')
    score = models.IntegerField()
    is_blacklisted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"
    
class Savings(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='savings')
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    purpose = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_progress = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_saved} (Start: {self.start_date}, End: {self.end_date})"

    class Meta:
        ordering = ['-created_at']
        

class Loan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loans',null=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    duration_months = models.IntegerField(null=True)
    application_date = models.DateField(default=timezone.now)
    repaid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    disbursed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    purpose = models.TextField(blank=True, null=True)
    collateral = models.CharField(max_length=255, blank=True, null=True)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grace_period_months = models.IntegerField(default=0)
    overdue_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overdue_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    due_date = models.DateField(null=True, blank=True)  # Add due_date field
    repayments = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_remaining_amount(self):
        return max(self.amount - self.repaid_amount, 0)

    def make_repayment(self, amount_paid):
        remaining_amount = self.calculate_remaining_amount()
        if amount_paid > remaining_amount:
            excess_amount = amount_paid - remaining_amount
            amount_paid = remaining_amount

        self.repaid_amount += amount_paid
        self.total_paid += amount_paid
        self.repayments += amount_paid
        self.save()

        if self.repaid_amount == self.amount:
            self.is_active = False
            self.save()

        return amount_paid
    def get_remaining_balance(self):
        return self.amount - self.repaid_amount

    def __str__(self):
        return f"Loan for {self.user.username} - Amount: {self.amount}"


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_repayments')  # Corrected related_name
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Repayment of {self.amount_paid} for Loan {self.loan.id}"
    
class Item(models.Model):
    name = models.CharField(max_length=255)
    loan_count = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    

class LoanItem(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name='loan_items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='loaned_items')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_loaned = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    condition_on_return = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item.name} on loan {self.loan.id} - Paid: {self.amount_paid}"

    class Meta:
        unique_together = ('loan', 'item')
        
class Payment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    is_loan_payment = models.BooleanField(default=False)
    is_savings_payment = models.BooleanField(default=False)
    loan = models.ForeignKey('Loan', on_delete=models.SET_NULL, null=True, blank=True, related_name='loan_payments')
    savings = models.ForeignKey('Savings', on_delete=models.SET_NULL, null=True, blank=True, related_name='savings_payments')
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment by {self.user.username} on {self.date} - Amount: {self.amount}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_loan_payment=True, is_savings_payment=False) |
                       models.Q(is_loan_payment=False, is_savings_payment=True),
                name='payment_for_loan_or_savings_only'
            ),
        ]
        
class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=[('income', 'Income'), ('expense', 'Expense')])
    timestamp = models.DateTimeField(default=timezone.now)
    loan = models.ForeignKey('Loan', on_delete=models.SET_NULL, null=True, blank=True, related_name='loan_transactions')
    savings = models.ForeignKey('Savings', on_delete=models.SET_NULL, null=True, blank=True, related_name='savings_transactions')
    category = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"Transaction by {self.user.username} - Amount: {self.amount} - Type: {self.transaction_type}"

    class Meta:
        ordering = ['-timestamp']
        
        

class SavingsItem(models.Model):
    savings = models.ForeignKey('Savings', on_delete=models.CASCADE, related_name='savings_items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='item_savings')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.name} for {self.savings.user.username} - Target: {self.target_amount}"

    class Meta:
        unique_together = (('savings', 'item'),)
        ordering = ['due_date']