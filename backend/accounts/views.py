from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserUpdateSerializer

User = get_user_model()

class CurrentUserView(APIView):
    """Get current user details"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UpdateUserProfileView(generics.UpdateAPIView):
    """Update user profile"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        
        response_serializer = UserSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)