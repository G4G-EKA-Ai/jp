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

from jaytipargal.asgi import application as app

print("[JAYTI] Django ASGI application ready on port 8001")
