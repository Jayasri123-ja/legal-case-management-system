from django.db import models
from django.conf import settings
from cases.models import Case

class Hearing(models.Model):
    """Model to store court hearings with email reminder tracking"""
    
    HEARING_TYPES = (
        ('hearing', 'Hearing'),
        ('meeting', 'Meeting'),
        ('deadline', 'Deadline'),
        ('trial', 'Trial'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    )
    
    
    title = models.CharField(max_length=200)
    hearing_type = models.CharField(max_length=20, choices=HEARING_TYPES, default='hearing')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='hearings')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_hearings'
    )
    
    # Hearing Details
    hearing_date = models.DateTimeField()
    duration = models.DurationField(blank=True, null=True, help_text="Expected duration of hearing")
    court = models.CharField(max_length=200)
    judge = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    # Reminder Tracking (only 2-hour reminder)
    reminder_2h_sent = models.BooleanField(default=False)
    
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['hearing_date']
        indexes = [
            models.Index(fields=['hearing_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.case.case_number} - {self.title} ({self.hearing_date.strftime('%d %b %Y')})"
    
    @property
    def is_upcoming(self):
        """Check if hearing is in the future"""
        from django.utils import timezone
        return self.hearing_date > timezone.now()
    
    @property
    def needs_2h_reminder(self):
        """Check if 2-hour reminder should be sent"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.reminder_2h_sent:
            return False
        
        time_diff = self.hearing_date - timezone.now()
        return timedelta(hours=1, minutes=50) <= time_diff <= timedelta(hours=2, minutes=10)