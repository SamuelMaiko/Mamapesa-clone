from django.contrib import admin
from .models import TrustScore, Savings, Loan, Item, LoanItem, Transaction, SavingsItem
from django.contrib.auth.admin import UserAdmin
from .models import SavingsPayment, LoanPayment

admin.site.register(TrustScore)
# admin.site.register(Payment)
admin.site.register(Transaction)
admin.site.register(LoanItem)
# customized
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'loan_count', 'in_stock')
    list_filter = ('in_stock',)
    search_fields = ('name', 'description')

admin.site.register(Item, ItemAdmin)

class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'interest_rate', 'duration_months', 'is_approved', 'is_active', 'disbursed')
    list_filter = ('is_approved', 'is_active', 'disbursed')
    search_fields = ('user__username', 'idnumber')

admin.site.register(Loan, LoanAdmin)

class SavingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_saved', 'start_date', 'end_date', 'in_progress')
    list_filter = ('is_active',)
    search_fields = ('user__username',)

admin.site.register(Savings, SavingsAdmin)
from .models import CustomUser

class CustomUserAdmin(UserAdmin): 
    model = CustomUser
    list_display = [ 'username',]
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('custom_field',)}),  # Add your custom fields in this tuple
    # )
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {'fields': ('custom_field',)}),  # Add your custom fields here for the create user page
    # )

admin.site.register(CustomUser, CustomUserAdmin)   


@admin.register(SavingsPayment)
class SavingsPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'savings', 'amount', 'date', 'is_successful')
    list_filter = ('is_successful',)
    search_fields = ('user__username', 'savings__id', 'reference_number')

@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan', 'amount', 'date', 'is_successful')
    list_filter = ('is_successful',)
    search_fields = ('user__username', 'loan__id', 'reference_number')

from .models import UserDetails

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'identification_number', 'phone_number', 'nationality', 'physical_address']
    search_fields = ['user__username', 'identification_number', 'phone_number']