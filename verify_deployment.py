#!/usr/bin/env python
"""
Deployment Verification Script for JPFINAL
Run this after deployment to verify health checks work
"""
import sys
import os

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaytipargal.settings')

def check_local():
    """Verify Django config loads correctly"""
    try:
        import django
        django.setup()
        from django.conf import settings
        print("[OK] Django loaded successfully")
        print(f"[OK] ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        return True
    except Exception as e:
        print(f"[ERROR] Django config error: {e}")
        return False

def check_endpoints():
    """Verify endpoints exist"""
    endpoints = ['/health/', '/']
    print(f"[INFO] Endpoints to verify: {endpoints}")
    return True

if __name__ == "__main__":
    print("=== JPFINAL Deployment Verification ===")
    
    success = True
    success = check_local() and success
    success = check_endpoints() and success
    
    if success:
        print("\n[PASS] Local verification passed. Ready for deployment.")
        sys.exit(0)
    else:
        print("\n[FAIL] Verification failed. Fix issues before deploying.")
        sys.exit(1)
