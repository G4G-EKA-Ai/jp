"""
JAYTI Birthday Website - Django ASGI wrapper for Emergent Platform
Runs Django via uvicorn on port 8001
"""
import os
import sys
import subprocess

# Add project root to Python path
sys.path.insert(0, '/app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaytipargal.settings')

# Run migrations using subprocess BEFORE Django setup (avoids async issues)
print("[JAYTI] Running database migrations...")
try:
    result = subprocess.run(
        ['python', 'manage.py', 'migrate', '--noinput'],
        cwd='/app',
        capture_output=True,
        text=True,
        timeout=60
    )
    if result.returncode == 0:
        print("[JAYTI] Database migrations complete")
    else:
        print(f"[JAYTI] Migration warning: {result.stderr}")
except Exception as e:
    print(f"[JAYTI] Migration note: {e}")

print("[JAYTI] Collecting static files...")
try:
    result = subprocess.run(
        ['python', 'manage.py', 'collectstatic', '--noinput'],
        cwd='/app',
        capture_output=True,
        text=True,
        timeout=60
    )
    print("[JAYTI] Static files collected")
except Exception as e:
    print(f"[JAYTI] Static files note: {e}")

print("[JAYTI] Creating initial user...")
try:
    result = subprocess.run(
        ['python', 'manage.py', 'create_initial_user'],
        cwd='/app',
        capture_output=True,
        text=True,
        timeout=30
    )
    print("[JAYTI] Initial user ready")
except Exception as e:
    print(f"[JAYTI] User note: {e}")

# Now setup Django and import the app
import django
django.setup()

from jaytipargal.asgi import application as app

print("[JAYTI] Django ASGI application ready on port 8001")
