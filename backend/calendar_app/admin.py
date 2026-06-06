from django.contrib import admin
from .models import Hearing

@admin.register(Hearing)
class HearingAdmin(admin.ModelAdmin):
    list_display = ('title', 'case', 'hearing_date', 'court', 'status')
    list_filter = ('status', 'hearing_type', 'hearing_date')
    search_fields = ('title', 'case__case_number', 'court')
    date_hierarchy = 'hearing_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'hearing_type', 'status', 'case')
        }),
        ('Schedule', {
            'fields': ('hearing_date', 'duration', 'court', 'judge')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_by'),
            'classes': ('collapse',)
        }),
        ('Reminder Tracking', {
            'fields': ('reminder_2h_sent',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'reminder_2h_sent')