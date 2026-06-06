from rest_framework import serializers
from .models import Hearing
from cases.serializers import CaseSerializer

class HearingSerializer(serializers.ModelSerializer):
    case_details = CaseSerializer(source='case', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Hearing
        fields = [
            'id', 'title', 'hearing_type', 'status',
            'case', 'case_details', 'created_by', 'created_by_name',
            'hearing_date', 'duration', 'court', 'judge', 'notes',
            'reminder_2h_sent',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'reminder_2h_sent']
    
    def validate_hearing_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Hearing date must be in the future")
        return value