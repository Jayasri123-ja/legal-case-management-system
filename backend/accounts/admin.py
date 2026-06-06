from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'firm', 'role', 'avatar')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'firm', 'role')}),
    )

admin.site.register(User, CustomUserAdmin)