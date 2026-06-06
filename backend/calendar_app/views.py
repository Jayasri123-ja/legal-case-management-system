from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Hearing
from .serializers import HearingSerializer
from .services import HearingReminderService
import django

class HearingViewSet(viewsets.ModelViewSet):
    queryset = Hearing.objects.all()
    serializer_class = HearingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'hearing_type', 'case']
    search_fields = ['title', 'court', 'judge', 'case__case_number', 'case__title']
    ordering_fields = ['hearing_date', 'created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Hearing.objects.all()
        return Hearing.objects.filter(
            django.db.models.Q(case__assigned_to=user) | 
            django.db.models.Q(case__created_by=user) |
            django.db.models.Q(created_by=user)
        ).distinct()
    
    def perform_create(self, serializer):
        hearing = serializer.save(created_by=self.request.user)
        print(f"✅ Hearing created: {hearing.title}")
        print(f"   ⏰ 2-hour reminder will be sent when calendar page loads or when reminder check is triggered")
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        hearing = self.get_object()
        hearing.status = 'completed'
        hearing.save()
        return Response({'status': 'Hearing marked as completed'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        hearing = self.get_object()
        hearing.status = 'cancelled'
        hearing.save()
        return Response({'status': 'Hearing cancelled'})
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        hearings = self.get_queryset().filter(
            hearing_date__gte=timezone.now(),
            status='scheduled'
        ).order_by('hearing_date')[:10]
        serializer = self.get_serializer(hearings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        today_start = timezone.now().replace(hour=0, minute=0, second=0)
        today_end = today_start + timedelta(days=1)
        hearings = self.get_queryset().filter(
            hearing_date__range=[today_start, today_end]
        ).order_by('hearing_date')
        serializer = self.get_serializer(hearings, many=True)
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['get'])
    def check_and_send_reminders(self, request):
        """Check for hearings that need reminders and send emails (triggered by frontend)"""
        print("🔍 Manual reminder check triggered from frontend")
        HearingReminderService.send_pending_reminders()
        return Response({'status': 'Reminder check completed'})
    
    
    @action(detail=False, methods=['get'])
    def needs_reminders(self, request):
        """Get hearings that need reminders (for debugging)"""
        now = timezone.now()
        
        hearings_2h = Hearing.objects.filter(
            hearing_date__range=[
                now + timedelta(hours=1, minutes=50),
                now + timedelta(hours=2, minutes=10)
            ],
            reminder_2h_sent=False,
            status='scheduled'
        )
        
        result = {
            '2h': HearingSerializer(hearings_2h, many=True).data
        }
        return Response(result)