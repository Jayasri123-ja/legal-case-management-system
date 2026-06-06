from django.db import models
from django.conf import settings
from cases.models import Case
from clients.models import Client
from documents.models import Document

class Activity(models.Model):
    """Model to track all system activities"""
    
    ACTIVITY_TYPES = (
        ('case', 'Case Activity'),
        ('file', 'File Activity'),
        ('client', 'Client Activity'),
        ('system', 'System Activity'),
        ('user', 'User Activity'),
    )
    
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('info', 'Info'),
    )
    
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    action = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, blank=True)
    
    # Optional relations
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    
    case_title = models.CharField(max_length=200, blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    document_name = models.CharField(max_length=200, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='info')
    metadata = models.JSONField(default=dict, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['type']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.type} - {self.action} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        
        if self.user and not self.username:
            self.username = self.user.get_full_name() or self.user.username
        super().save(*args, **kwargs)