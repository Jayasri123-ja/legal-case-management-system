from django.db import models
from django.conf import settings
from cases.models import Case
import os

class Document(models.Model):
    """Model to store uploaded legal documents"""
    
    DOCUMENT_TYPES = (
        ('petition', 'Petition'),
        ('evidence', 'Evidence'),
        ('judgment', 'Judgment'),
        ('contract', 'Contract'),
        ('pleading', 'Pleading'),
        ('other', 'Other'),
    )
    
    
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    file_size = models.IntegerField(help_text="File size in bytes", blank=True, null=True)
    file_type = models.CharField(max_length=50, blank=True)
    
   
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='other')
    description = models.TextField(blank=True)
    
   
    extracted_text = models.TextField(blank=True, help_text="Raw text extracted from document")
    summary = models.TextField(blank=True, help_text="AI-generated summary")  # Changed to TextField
    key_entities = models.JSONField(default=dict, blank=True, help_text="Extracted entities like dates, people, laws")
    
    
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.file.name)
    
    class Meta:
        ordering = ['-uploaded_at']