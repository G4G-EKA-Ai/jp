"""
JAYTI Birthday Website - Django ASGI wrapper for Emergent Platform
Runs Django via uvicorn on port 8001
"""
import os
import sys
import threading

# Add project root to Python path
sys.path.insert(0, '/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaytipargal.settings')

import django
django.setup()

# Run migrations and setup in a background thread (non-blocking)
def run_setup():
    from django.core.management import call_command
    try:
        call_command('migrate', '--noinput', verbosity=0)
        print("[JAYTI] Database migrations complete")
    except Exception as e:
        print(f"[JAYTI] Migration note: {e}")
    
    try:
        call_command('create_initial_user')
    except Exception as e:
        print(f"[JAYTI] User creation note: {e}")
    
    try:
        call_command('collectstatic', '--noinput', verbosity=0)
        print("[JAYTI] Static files collected")
    except Exception as e:
        print(f"[JAYTI] Static files note: {e}")
    
    try:
        call_command('loaddata', 'initial_data', verbosity=0)
        print("[JAYTI] Initial data loaded")
    except Exception as e:
        print(f"[JAYTI] Fixture note: {e}")

setup_thread = threading.Thread(target=run_setup, daemon=True)
setup_thread.start()

from jaytipargal.asgi import application as app

print("[JAYTI] Django ASGI application ready on port 8001")
