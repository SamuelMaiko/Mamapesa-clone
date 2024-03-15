from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import Sum, F
from datetime import timedelta, date, datetime
from decimal import Decimal
from django.conf import settings
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser, PermissionsMixin):
    phone_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    username = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'phone_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    class Meta:
        db_table="Users"

    def __str__(self):
        return self.phone_number
    

class Communication(models.Model):
    COMMUNICATION_TYPES = [
        ('loan_submission', 'Loan Submission'),
        ('loan_approval', 'Loan Approval'),
        ('loan_rejection', 'Loan Rejection'),
        ('loan_disbursement', 'Loan Disbursement'),
        ('loan_payment', 'Loan Payment'),
        ('savings_deposit', 'Savings Deposit'),
        ('savings_withdrawal', 'Savings Withdrawal'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    
    class Meta:
        db_table="Communications"

    def __str__(self):
        return f"{self.get_communication_type_display()} for {self.user.username} at {self.timestamp}"