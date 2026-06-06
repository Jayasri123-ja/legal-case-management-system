from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Activity
from .serializers import ActivitySerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for activities (read-only)"""
    
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'user']
    search_fields = ['action', 'description', 'username', 'case_title', 'client_name']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        """Filter by time range if specified"""
        queryset = super().get_queryset()
        
       
        time_range = self.request.query_params.get('time_range', 'all')
        if time_range == 'today':
            queryset = queryset.filter(timestamp__date=timezone.now().date())
        elif time_range == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(timestamp__gte=week_ago)
        elif time_range == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(timestamp__gte=month_ago)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity statistics"""
        queryset = self.get_queryset()
        today = timezone.now().date()
        
        return Response({
            'total': queryset.count(),
            'today': queryset.filter(timestamp__date=today).count(),
            'cases': queryset.filter(type='case').count(),
            'files': queryset.filter(type='file').count(),
            'clients': queryset.filter(type='client').count(),
            'system': queryset.filter(type='system').count(),
        })