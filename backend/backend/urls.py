from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('clients.urls')),
    path('api/', include('cases.urls')),
    path('api/', include('documents.urls')),  
    path('api/auth/', include('accounts.urls')),
    path('api/', include('calendar_app.urls')),  
    path('api/', include('activities.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)