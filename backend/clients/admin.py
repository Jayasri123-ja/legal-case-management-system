from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'client_type', 'status', 'created_at')
    list_filter = ('client_type', 'status', 'country')
    search_fields = ('name', 'email', 'phone', 'company')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'company', 'client_type')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )