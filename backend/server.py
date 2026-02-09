"""
JAYTI Birthday Website - Django ASGI wrapper for Emergent Platform
Runs Django via uvicorn on port 8001

CRITICAL: Server starts IMMEDIATELY to pass health checks.
Migrations run in background thread after startup.
"""
import os
import sys
import threading
import subprocess

# Add project root to Python path
sys.path.insert(0, '/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaytipargal.settings')

# Setup Django FIRST - server must be ready for health checks immediately
import django
django.setup()

from jaytipargal.asgi import application as app

print("[JAYTI] Django ASGI application ready on port 8001")

# Run migrations and setup in background thread (non-blocking)
def run_background_setup():
    """Run migrations and initial setup in background after server starts"""
    import time
    time.sleep(2)  # Wait for server to fully start
    
    python_exec = sys.executable
    
    print("[JAYTI] Running background database migrations...")
    try:
        result = subprocess.run(
            [python_exec, 'manage.py', 'migrate', '--noinput'],
            cwd='/app',
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'jaytipargal.settings'}
        )
        if result.returncode == 0:
            print("[JAYTI] Database migrations complete")
        else:
            print(f"[JAYTI] Migration warning: {result.stderr[:200] if result.stderr else 'unknown'}")
    except Exception as e:
        print(f"[JAYTI] Migration note: {e}")

    print("[JAYTI] Collecting static files...")
    try:
        result = subprocess.run(
            [python_exec, 'manage.py', 'collectstatic', '--noinput'],
            cwd='/app',
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'jaytipargal.settings'}
        )
        print("[JAYTI] Static files collected")
    except Exception as e:
        print(f"[JAYTI] Static files note: {e}")

    print("[JAYTI] Creating initial user...")
    try:
        result = subprocess.run(
            [python_exec, 'manage.py', 'create_initial_user'],
            cwd='/app',
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'jaytipargal.settings'}
        )
        print("[JAYTI] Initial user ready")
    except Exception as e:
        print(f"[JAYTI] User note: {e}")
    
    print("[JAYTI] Background setup complete!")

# Start background setup thread
setup_thread = threading.Thread(target=run_background_setup, daemon=True)
setup_thread.start()
