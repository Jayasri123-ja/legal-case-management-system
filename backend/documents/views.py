from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document
from .serializers import DocumentSerializer
from .gemini_summarizer import GeminiSummarizer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        document = serializer.save(uploaded_by=self.request.user)
        
        if document.file:
            document.file_size = document.file.size
            file_name = document.file.name
            if file_name.endswith('.pdf'):
                document.file_type = 'pdf'
            elif file_name.endswith('.doc'):
                document.file_type = 'doc'
            elif file_name.endswith('.docx'):
                document.file_type = 'docx'
            document.save()
            
            # Use the REAL AI summarizer
            processor = GeminiSummarizer()
            processor.process_document(document)  # <-- This was indented wrong
    
    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        document = self.get_object()  # <-- Need indentation here
        processor = GeminiSummarizer()
        success = processor.process_document(document)
        
        if success:
            return Response({'status': 'Document reprocessed successfully'})
        else:
            return Response(
                {'error': document.processing_error},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = Document.objects.count()
        processed = Document.objects.filter(is_processed=True).count()
        pending = Document.objects.filter(is_processed=False).exclude(processing_error__gt='').count()
        failed = Document.objects.exclude(processing_error='').count()
        
        return Response({
            'total': total,
            'processed': processed,
            'pending': pending,
            'failed': failed,
        })