from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model with additional fields"""
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('lawyer', 'Lawyer'),
        ('paralegal', 'Paralegal'),
        ('client', 'Client'),
    )
    
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    firm = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='lawyer')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"
    
    class Meta:
        db_table = 'auth_user'  # This will replace the default auth_user table