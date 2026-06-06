from django.db import models
from django.conf import settings
from clients.models import Client

class Case(models.Model):
    """Case model to store legal case information"""
    
    CASE_TYPE_CHOICES = (
        ('civil', 'Civil'),
        ('criminal', 'Criminal'),
        ('corporate', 'Corporate'),
        ('family', 'Family'),
        ('property', 'Property'),
        ('intellectual', 'Intellectual Property'),
        ('employment', 'Employment'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('archived', 'Archived'),
    )
    
    
    title = models.CharField(max_length=200)
    case_number = models.CharField(max_length=50, unique=True)
    
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cases')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_cases')
    
    
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField(blank=True, null=True)
    
    
    filed_date = models.DateField()
    closing_date = models.DateField(blank=True, null=True)
    
    
    court_name = models.CharField(max_length=200, blank=True, null=True)
    judge_name = models.CharField(max_length=200, blank=True, null=True)
    
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='cases_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.case_number} - {self.title}"
    
    class Meta:
        ordering = ['-filed_date', '-created_at']