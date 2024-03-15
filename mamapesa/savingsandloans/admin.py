from django.contrib import admin
from .models import Savings, Item, SavingsItem, PaymentMethod, Customer, Payment, Currency, Loan

# Register your models here.


admin.site.register(Loan)
admin.site.register(PaymentMethod)
admin.site.register(Currency)
admin.site.register(Payment)
admin.site.register(Item)
admin.site.register(Savings)
admin.site.register(Customer)
admin.site.register(SavingsItem)
