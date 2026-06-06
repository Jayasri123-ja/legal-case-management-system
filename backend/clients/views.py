from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for clients
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def cases(self, request, pk=None):
        """Get all cases for a specific client"""
        client = self.get_object()
        cases = client.cases.all()
        from cases.serializers import CaseSerializer
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data)