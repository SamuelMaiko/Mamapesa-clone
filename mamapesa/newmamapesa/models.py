from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import timedelta, date
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



class CustomUser(AbstractUser):
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    idnumber = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email=models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)  # Add interest_rate field
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
    loan_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_limit = models.DecimalField(max_digits=10, decimal_places=2, default=8000)  # Add loan_limit field
   # savings_account = models.ForeignKey('Savings', on_delete=models.CASCADE, related_name='savings_accounts', null=True, blank=True)

    class Meta:
        db_table="Users"

    def save(self, *args, **kwargs):
       
        if self.loan_limit is None or self.loan_limit == 0:
            self.loan_limit = 8000
        super().save(*args, **kwargs)

    def __str__(self):

        return self.username
    
class UserDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='details')
    identification_number = models.CharField(max_length=20, unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15)
    nationality = models.CharField(max_length=50)
    physical_address = models.TextField()
    
    def __str__(self):
        return f"Details for {self.user.username}"
    
class TrustScore(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='their_trust_score')
    score = models.IntegerField()
    is_blacklisted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"
    
    class Meta:
        db_table="TrustScore"
 
class Item(models.Model):
    name = models.CharField(max_length=255)
    loan_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)   
    description = models.TextField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.name 
    class Meta:
        db_table="Items"  
class Savings(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='savings')
    user=models.OneToOneField(CustomUser , on_delete=models.CASCADE, related_name="savings_account")
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_savings')
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(default=timezone.now)
    # end_date = models.DateField()
    # purpose = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # in_progress = models.BooleanField(default=True)
    items=models.ManyToManyField(Item ,through="SavingsItem", related_name="savings")

    def __str__(self):
        return f"{self.user.username} - {self.amount_saved} (Start: {self.start_date})"

    class Meta:
        ordering = ['-created_at']
        db_table="Savings_Accounts"
        


# class LoanManager(models.Manager):
#     def get_active_loan(self, user):
#         return self.filter(user=user, is_active=True).first()      

class Loan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.TextField(blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    loan_duration = models.IntegerField(default = 90)
    application_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)  # Add due_date field
    repaid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    disbursed = models.BooleanField(default=False)
    grace_period = models.IntegerField(default=30)
    grace_period_end_date = models.DateField(null=True, blank=True)  # Add due_date field
    late_payment_penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    collateral = models.FileField(upload_to='collaterals/', blank=True, null=True)
    amount_disbursed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user.username}'s  loan {self.id} of Kshs.{self.amount}"
    class Meta:
            db_table="Loans"
    #remaining_days = models.IntegerField(default=90)
    # grace_period_remaining_days = models.IntegerField(default=30)
    # overdue_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # overdue_fee = models.DecimalField(max_digits=10, decimal_places=2)
    # repayments = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # helper function to calculte amount disbursed in save() method
    
    class Meta:
        ordering=["-due_date"]
        
    def generate_amount_disbursed(self):
        interest_rate = Decimal(str(self.interest_rate))
        self.amount_disbursed = self.amount * (1 - interest_rate / 100)

    # override save() method        ````
    def save(self, *args, **kwargs):
       
       self.due_date=self.application_date + timedelta(days=self.loan_duration)

       self.generate_amount_disbursed()
       
       
       if self.repaid_amount>=self.amount:
           self.is_active=False
        
        

       if self.is_repayment_due:
           today=date.today()
           self.grace_period_end_date=today+timedelta(self.grace_period)

       return super().save(*args, **kwargs) 
   
   
    
    def is_fully_repaid(self):
        return self.repaid_amount == self.amount
    
    def calculate_remaining_amount(self):
        return self.amount - self.repaid_amount
    
    @property
    def remaining_amount(self):
        return self.amount - self.repaid_amount
    
    @property
    def remaining_days(self):
        today=date.today()
        return self.due_date-today
   
    @property
    def grace_period_remaining_days(self):
        today=date.today()

        if self.grace_period_end_date:
            return self.grace_period_end_date-today
        else:
            return None
    @property 
    def is_repayment_due(self):
        today=date.today()

        return today>=self.due_date
    
    # amount crossed over to the grace period
    @property
    def overdue_amount(self):
        overdue_amount=self.amount-self.repaid_amount
        if not self.overdue_fee>=0:
            overdue_amount+=self.overdue_fee

        return overdue_amount

    @property
    def overdue_fee(self):
        if self.grace_period_end_date:
            overdue_fee=self.overdue_amount*(self.late_payment_penalty_rate/100)
        else:
            overdue_fee=0
        return overdue_fee
    


    # duration_months = models.IntegerField(default = 3)
    # duration_months = models.IntegerField(default = 3)
    # total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # loan_limit = models.DecimalField(max_digits=10, decimal_places=2, default=8000)
    #installment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # grace_period_months = models.IntegerField(default=1)
    # grace_period = models.IntegerField(default=30)
    # penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # loan_owed = models.DecimalField(max_digits = 10, decimal_places=2,default= 0)



class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_repayments')  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date=models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # overriding to update parent loan instance repaid_amount
    def save(self, *args, **kwargs):

        self.loan.repaid_amount+=self.amount_paid
        self.loan.save()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Repayment of {self.amount_paid} for Loan {self.loan.id}" 
    
    class Meta:
        db_table="Loan_Repayments"      
        
class LoanTransaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loan_transactions')
    type = models.CharField(max_length=20, choices=[('REPAY', 'repay'), ('LOAN_DISBURSEMENT', 'loan_disbursement')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True, default="")
    timestamp = models.DateTimeField(default=timezone.now)
    loan = models.ForeignKey('Loan', on_delete=models.SET_NULL, null=True, blank=True, related_name='loan_transactions')
    is_successful = models.BooleanField(default=True)
    # savings = models.ForeignKey('Savings', on_delete=models.SET_NULL, null=True, blank=True, related_name='savings_transactions')
    # category = models.CharField(max_length=50, blank=True, null=True)
    #payment_method = models.CharField(max_length=50, blank=True, null=True)
    # reference_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Transaction by {self.user.username} - Amount: {self.amount}"

    class Meta:
        ordering = ['-timestamp']
        db_table="Loan_Transactions"

    
class SavingsItem(models.Model):
    savings = models.ForeignKey('Savings', on_delete=models.CASCADE, related_name='savings_items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='savings_items')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    achieved = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=True)
    saving_period=models.IntegerField(default=90)
    is_suspended=models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.item.name} for {self.savings.user.username} - Target: {self.target_amount}"

    class Meta:
        unique_together = (('savings', 'item'),)
        ordering = ['due_date']
        db_table="Savings_Items"
        
    def save(self, *args, **kwargs):
        if self.amount_saved>=self.target_amount:
            self.achieved=True
            # self.in_progress
        
        if self.start_date:
            self.due_date = self.start_date + timedelta(days=self.saving_period)
        super().save(*args, **kwargs)
        
    @property
    def is_target_amount_reached(self):
        return self.amount_saved>=self.target_amount
    
    @property
    def remaining_amount(self):
        return self.target_amount-self.amount_saved
    
    @property
    def installment(self):
        return round(self.target_amount/self.saving_period, 2)
        
    def amount_skipped(self):
        balance=self.target_amount-self.amount_saved
        remaining_amount_to_target=self.remaining_days*self.installment
        return balance-remaining_amount_to_target
    
    @property
    def days_payment(self):
        remaining_day=self.remaining_days-1
        # if self.remaining_days is not None:
        #     remaining_day = self.remaining_days - 1
        # else:
        #     # Handle the case where self.remaining_days is None
        #     remaining_day = None
        cash=remaining_day*self.installment
        total=cash+self.amount_saved
        return round(self.target_amount-total, 2)

    @property
    def is_achieved(self):
        if self.amount_saved>=self.target_amount:
            self.achieved=True
            self.in_progress=False
            self.save()
            return True
        else:
            self.achieved=False
            self.in_progress=True
            self.save()
            return False
    
    @property
    def remaining_days(self):
        """Calculate the number of days remaining until the savings goal is reached."""
        if self.due_date:
            today = date.today()
            today = today + timedelta(days=10)
            remaining_days = (self.due_date - today).days
            return max(0, remaining_days)
        else:
            return None

    

class PaymentMethod(models.Model):
    name=models.CharField(max_length=30)
    # display_name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    icon=models.ImageField(upload_to='payment_icons/', null=True, blank=True)
    active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table="Payment_Methods"
        
    def __str__(self):
        return f"{self.name} payment method"
        
class SavingsTransaction(models.Model):
    TRANSACTION_TYPES=[
        ("WITHDRAWAL", "withdrawal"),
        ("DEPOSIT", "deposit"),
    ]
    type=models.CharField(max_length=25, choices=TRANSACTION_TYPES)
    amount=models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    savings_item=models.ForeignKey(SavingsItem, on_delete=models.CASCADE, related_name="transactions")
    payment_method=models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.savings_item.savings.user.username}'s transaction of {self.amount} on {self.timestamp}"
    class Meta:
        db_table="Savings_Transactions"
        ordering=['-timestamp',]
    
  