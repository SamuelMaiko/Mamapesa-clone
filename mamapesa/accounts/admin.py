from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


# Register your models here.
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
