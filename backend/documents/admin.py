from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'case', 'uploaded_by', 'document_type', 'is_processed', 'uploaded_at')
    list_filter = ('is_processed', 'document_type', 'uploaded_at')
    search_fields = ('title', 'description', 'summary')
    readonly_fields = ('file_size', 'file_type', 'extracted_text', 'summary', 
                      'key_entities', 'is_processed', 'processed_at', 'processing_error')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'file', 'case', 'uploaded_by', 'document_type', 'description')
        }),
        ('File Info', {
            'fields': ('file_size', 'file_type'),
            'classes': ('collapse',)
        }),
        ('Analysis Results', {
            'fields': ('is_processed', 'processed_at', 'processing_error', 
                      'extracted_text', 'summary', 'key_entities'),
            'classes': ('collapse',)
        }),
    )