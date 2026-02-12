"""
Custom middleware for CSRF handling in production
"""
from django.conf import settings


class DynamicCSRFMiddleware:
    """
    Middleware that dynamically adds the request's Host to CSRF_TRUSTED_ORIGINS.
    This helps with production deployments where the exact domain may vary.
    
    CRITICAL: Skips processing for health check endpoints to ensure fast response
    during Kubernetes probes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # CRITICAL: Skip all processing for health checks - respond immediately
        if request.path.rstrip('/') == '/health':
            return self.get_response(request)
        
        # Get the host from the request
        host = request.get_host()
        
        # Build the origin
        scheme = 'https' if request.is_secure() else 'http'
        origin = f'{scheme}://{host}'
        
        # Add to CSRF_TRUSTED_ORIGINS if not already present
        if origin not in settings.CSRF_TRUSTED_ORIGINS:
            settings.CSRF_TRUSTED_ORIGINS.append(origin)
        
        # Also add https version if not secure (in case of proxy)
        https_origin = f'https://{host}'
        if https_origin not in settings.CSRF_TRUSTED_ORIGINS:
            settings.CSRF_TRUSTED_ORIGINS.append(https_origin)
        
        response = self.get_response(request)
        return response
