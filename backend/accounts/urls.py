from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', views.CurrentUserView.as_view(), name='current_user'),
    path('users/me/update/', views.UpdateUserProfileView.as_view(), name='update_user'),  # Add this
]