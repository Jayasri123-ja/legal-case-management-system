from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'firm')
        read_only_fields = ('id', 'username')

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'firm', 'role')
    
    def validate_email(self, value):
        """Ensure email is unique except for current user"""
        user = self.context.get('request').user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value