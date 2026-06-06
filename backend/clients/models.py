from django.db import models
from django.conf import settings

class Client(models.Model):
    """Client model to store client information"""
    
    CLIENT_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('government', 'Government'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('lead', 'Lead'),
    )
    
    
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    
   
    company = models.CharField(max_length=200, blank=True, null=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, default='individual')
    
    
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default='USA')
    
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='clients_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']