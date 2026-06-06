from rest_framework import serializers
from .models import Case
from clients.serializers import ClientSerializer

class CaseSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')