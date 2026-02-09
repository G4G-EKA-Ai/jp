"""
URL configuration for jaytipargal project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from datetime import datetime

def root_health_check(request):
    """
    Root-level health check for Kubernetes probes.
    CRITICAL: Must respond immediately without any DB operations.
    """
    return JsonResponse({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
    }, status=200)

urlpatterns = [
    # Health check at root level - responds BEFORE any middleware/DB
    path('health', root_health_check, name='root_health'),
    path('health/', root_health_check, name='root_health_slash'),
    
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('notes/', include('notes.urls')),
    path('diary/', include('diary.urls')),
    path('goals/', include('goals.urls')),
    path('astro/', include('astro.urls')),
    path('ai-chat/', include('ai_chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
