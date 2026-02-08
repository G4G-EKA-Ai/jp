"""
JAYTI Birthday Website - Django ASGI wrapper for Emergent Platform
Runs Django via uvicorn on port 8001
"""
import os
import sys

# Add project root to Python path
sys.path.insert(0, '/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaytipargal.settings')

import django
django.setup()

# Run migrations SYNCHRONOUSLY before starting (critical for deployment)
from django.core.management import call_command

print("[JAYTI] Running database migrations...")
try:
    call_command('migrate', '--noinput', verbosity=1)
    print("[JAYTI] Database migrations complete")
except Exception as e:
    print(f"[JAYTI] Migration error (non-fatal): {e}")

print("[JAYTI] Collecting static files...")
try:
    call_command('collectstatic', '--noinput', verbosity=0)
    print("[JAYTI] Static files collected")
except Exception as e:
    print(f"[JAYTI] Static files note: {e}")

print("[JAYTI] Creating initial user...")
try:
    call_command('create_initial_user')
    print("[JAYTI] Initial user ready")
except Exception as e:
    print(f"[JAYTI] User creation note: {e}")

from jaytipargal.asgi import application as app

print("[JAYTI] Django ASGI application ready on port 8001")
