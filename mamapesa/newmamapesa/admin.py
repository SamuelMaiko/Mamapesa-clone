from django.contrib import admin
from .models import Savings, Item, SavingsItem, PaymentMethod, Customer, CustomUser, Payment, Currency
# from .models import TrustScore, Savings, Loan, Item, Payment, SavingsItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.admin import UserAdmin

# admin.site.register(TrustScore)
# admin.site.register(Payment)
# admin.site.register(Transaction)
# admin.site.register(LoanItem)
# admin.site.register(SavingsTransaction)
admin.site.register(PaymentMethod)
admin.site.register(Currency)
admin.site.register(Payment)
admin.site.register(Item)
admin.site.register(Savings)
admin.site.register(Customer)
admin.site.register(SavingsItem)  


class CustomUserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ('phone_number', 'email','first_name','last_name', 'username','is_active', 'is_staff', 'is_superuser')  # Display phone number in the user list
    fieldsets = (
        (None, {'fields': ('phone_number', 'password','email','first_name','last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)


# from .models import UserDetails

# @admin.register(UserDetails)
# class UserDetailsAdmin(admin.ModelAdmin):
#     list_display = ['user', 'identification_number', 'phone_number', 'nationality', 'physical_address']
#     search_fields = ['user__username', 'identification_number', 'phone_number']