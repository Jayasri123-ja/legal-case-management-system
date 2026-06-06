from .services import ActivityLogger

class ActivityLoggingMixin:
    """Mixin to automatically log activities for model changes"""
    
    def log_creation(self, request, obj):
        """Log when object is created"""
        ActivityLogger.log_system_activity(
            action='create',
            description=f'{obj.__class__.__name__} created',
            status='success'
        )
    
    def log_update(self, request, obj):
        """Log when object is updated"""
        ActivityLogger.log_system_activity(
            action='update',
            description=f'{obj.__class__.__name__} updated',
            status='info'
        )
    
    def log_deletion(self, request, obj):
        """Log when object is deleted"""
        ActivityLogger.log_system_activity(
            action='delete',
            description=f'{obj.__class__.__name__} deleted',
            status='warning'
        )