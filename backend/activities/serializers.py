from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    
    user_name = serializers.CharField(source='username', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'type', 'action', 'description', 
            'user', 'user_name', 'username',
            'case', 'case_title', 'client', 'client_name',
            'document', 'document_name',
            'status', 'metadata', 'timestamp'
        ]