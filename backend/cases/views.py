from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Case
from .serializers import CaseSerializer

class CaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for cases
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'case_type', 'client']
    search_fields = ['title', 'case_number', 'client__name']
    ordering_fields = ['filed_date', 'created_at', 'status']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update case status"""
        case = self.get_object()
        new_status = request.data.get('status')
        if new_status:
            case.status = new_status
            case.save()
            return Response({'status': 'updated'})
        return Response({'error': 'status field required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def my_cases(self, request):
        """Get cases assigned to current user"""
        cases = Case.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(cases, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get case statistics"""
        total = Case.objects.count()
        active = Case.objects.filter(status='active').count()
        pending = Case.objects.filter(status='pending').count()
        closed = Case.objects.filter(status='closed').count()
        won = Case.objects.filter(status='won').count()
        lost = Case.objects.filter(status='lost').count()
        
        return Response({
            'total': total,
            'active': active,
            'pending': pending,
            'closed': closed,
            'won': won,
            'lost': lost,
        })