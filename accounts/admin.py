from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active_account', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active_account', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('MediBridge Role Info', {'fields': ('role', 'phone_number', 'is_active_account')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('MediBridge Role Info', {'fields': ('email', 'role', 'phone_number')}),
    )
