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
    loan_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0)


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
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='savings')
    user=models.OneToOneField(CustomUser , on_delete=models.CASCADE, related_name="savings_account")
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(default=timezone.now)
    # end_date = models.DateField()
    # purpose = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # in_progress = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_saved} (Start: {self.start_date})"

    class Meta:
        ordering = ['-created_at']

class LoanManager(models.Manager):
    def get_active_loan(self, user):
        return self.filter(user=user, is_active=True).first()      

class Loan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    duration_months = models.IntegerField(default = 3)
    loan_duration = models.IntegerField(default = 90)
    application_date = models.DateField(default=timezone.now)
    repaid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    disbursed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    purpose = models.TextField(blank=True, null=True)
    collateral = models.FileField(upload_to='collaterals/', blank=True, null=True)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grace_period_months = models.IntegerField(default=1)
    overdue_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overdue_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    due_date = models.DateField(null=True, blank=True)  # Add due_date field
    repayments = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_disbursed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loan_owed = models.DecimalField(max_digits = 10, decimal_places=2,default= 0)
    #is_collateralized = models.BooleanField(default=False)

    objects = LoanManager()

    def calculate_remaining_amount(self):
        return max(self.amount - self.repaid_amount, 0)


    def make_repayment(self, amount_paid):
        remaining_amount = self.calculate_remaining_amount()
        if amount_paid > remaining_amount:
            excess_amount = amount_paid - remaining_amount

            # if self.is_collateralized:
            #amount_paid = excess_amount
            
            user_savings = get_user_model().savings_account
            user_savings.amount_saved += excess_amount
            user_savings.save()

        self.repaid_amount += amount_paid
        self.total_paid += amount_paid
        self.repayments += amount_paid
        self.save()

        self.update_loan_status()
        return amount_paid

    def update_loan_status(self):
        if self.repaid_amount == self.amount:
            self.is_active = False
        elif 0 < self.loan_owed <= 8000:
            self.is_active = True
        else:
             self.is_active = False

        self.save()     

        
    def get_remaining_balance(self):
        return max(self.amount - self.repaid_amount, 0)
    
    @property
    def installment(self):
        installment_amount = self.amount/self.loan_duration
        return round(installment_amount, 2)
    
    def calculate_grace_period_remaining_days(self):
        if self.due_date:
            current_date = timezone.now().date()
            days_since_due = (current_date - self.due_date).days
            remaining_days = max(self.grace_period_days() - days_since_due, 0)
            return remaining_days
        return 0
    def is_within_grace_period(self):
        remaining_days = self.calculate_grace_period_remaining_days()
        return remaining_days > 0
        
    @property
    def grace_period_days(self):
        return self.grace_period_months * 30
    
    def calculate_overdue_amount(self):
        if self.is_overdue():
            overdue_days = (timezone.now().date() - self.due_date).days
            overdue_interest_rate = self.penalty_rate + self.overdue_rate
            overdue_amount = (self.loan_owed * overdue_interest_rate / 100) * (overdue_days / 30)
            return Decimal(overdue_amount).quantize(Decimal('0.01'))
        return Decimal(0)

    
    def is_overdue(self):
        return self.due_date and timezone.now().date() > self.due_date
    
    def __str__(self):
        return f"Loan for {self.user.username} - Amount: {self.amount}"

@receiver(post_save, sender=Loan)
def create_loan_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            user=instance.user,
            amount=instance.amount,
            description=f"Loan request for {instance.amount}",
            transaction_type='expense',
            loan=instance,
            is_successful=True
        )

class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_repayments')  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Repayment of {self.amount_paid} for Loan {self.loan.id}"
       

@receiver(post_save, sender=LoanRepayment)
def create_repayment_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            user=instance.loan.user,
            amount=instance.amount_paid,
            description=f"Loan repayment of {instance.amount_paid}",
            transaction_type='income',
            loan=instance.loan,
            is_successful=True
        )

    
class Item(models.Model):
    name = models.CharField(max_length=255)
    loan_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)   
    description = models.TextField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    savings=models.ManyToManyField(Savings, related_name="items")

    def __str__(self):
        return self.name
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
            # today = today + timedelta(days=1)
            remaining_days = (self.due_date - today).days
            return max(0, remaining_days)
        else:
            return None

    def __str__(self):
        return f"{self.item.name} for {self.savings.user.username} - Target: {self.target_amount}"

    class Meta:
        unique_together = (('savings', 'item'),)
        ordering = ['due_date']
    
    def save(self, *args, **kwargs):
        # Calculate due date by adding 90 days to start_date
        # if self.start_date and not self.due_date:
        # self.savings.amount_saved+=Decimal(round(self.amount_saved,2))
        # self.savings.save()
        
        if self.start_date:
            self.due_date = self.start_date + timedelta(days=self.saving_period)
        super().save(*args, **kwargs)
    

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
    #payment_method = models.CharField(max_length=50, blank=True, null=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"Transaction by {self.user.username} - Amount: {self.amount} - Type: {self.transaction_type}"

    class Meta:
        ordering = ['-timestamp']
        
        
