#!/usr/bin/env python3
"""Quick deployment verification script"""
import sys

# Check ALLOWED_HOSTS setting
try:
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaytipargal.settings')
    django.setup()
    
    from django.conf import settings
    
    print("✓ Django settings loaded")
    print(f"✓ ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    
    if settings.ALLOWED_HOSTS == ['*']:
        print("✓ ALLOWED_HOSTS correctly set to accept all hosts")
        print("✓ K8s health checks will work")
        sys.exit(0)
    else:
        print("✗ ALLOWED_HOSTS not set correctly")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
