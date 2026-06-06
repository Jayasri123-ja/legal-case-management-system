from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    case_title = serializers.CharField(source='case.title', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file', 'filename', 'file_size', 'file_type',
            'case', 'case_title', 'uploaded_by', 'uploaded_by_name',
            'document_type', 'description',
            'extracted_text', 'summary', 'key_entities',
            'is_processed', 'processing_error',
            'uploaded_at', 'processed_at'
        ]
        read_only_fields = ['file_size', 'file_type', 'extracted_text', 'summary', 
                           'key_entities', 'is_processed', 'processed_at', 'processing_error']
    
    def get_filename(self, obj):
        return obj.filename()