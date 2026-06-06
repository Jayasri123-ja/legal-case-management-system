from django.contrib import admin
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'title', 'client', 'case_type', 'status', 'filed_date')
    list_filter = ('case_type', 'status', 'filed_date')
    search_fields = ('case_number', 'title', 'client__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'case_number', 'client', 'assigned_to')
        }),
        ('Case Details', {
            'fields': ('case_type', 'status', 'description')
        }),
        ('Dates', {
            'fields': ('filed_date', 'closing_date')
        }),
        ('Court Information', {
            'fields': ('court_name', 'judge_name'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )