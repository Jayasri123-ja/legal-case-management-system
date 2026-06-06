from django.utils import timezone
from .models import Activity

class ActivityLogger:
    """Service to log activities throughout the system"""
    
    @staticmethod
    def log_case_activity(user, action, description, case=None, status='info'):
        """Log case-related activity"""
        Activity.objects.create(
            type='case',
            action=action,
            description=description,
            user=user,
            username=user.get_full_name() or user.username if user else 'System',
            case=case,
            case_title=case.title if case else '',
            status=status
        )
    
    @staticmethod
    def log_file_activity(user, action, description, document=None, status='info'):
        """Log file-related activity"""
        Activity.objects.create(
            type='file',
            action=action,
            description=description,
            user=user,
            username=user.get_full_name() or user.username if user else 'System',
            document=document,
            document_name=document.title if document else '',
            status=status
        )
    
    @staticmethod
    def log_client_activity(user, action, description, client=None, status='info'):
        """Log client-related activity"""
        Activity.objects.create(
            type='client',
            action=action,
            description=description,
            user=user,
            username=user.get_full_name() or user.username if user else 'System',
            client=client,
            client_name=client.name if client else '',
            status=status
        )
    
    @staticmethod
    def log_system_activity(action, description, status='info'):
        """Log system-related activity"""
        Activity.objects.create(
            type='system',
            action=action,
            description=description,
            username='System',
            status=status
        )
    
    @staticmethod
    def log_user_activity(user, action, description, status='info'):
        """Log user-related activity"""
        Activity.objects.create(
            type='user',
            action=action,
            description=description,
            user=user,
            username=user.get_full_name() or user.username if user else 'System',
            status=status
        )