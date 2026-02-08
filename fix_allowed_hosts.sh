#!/bin/bash
# Quick fix for ALLOWED_HOSTS issue
# Run this in Emergent terminal

echo "🔧 Fixing ALLOWED_HOSTS configuration..."

# Set environment variable for current session
export ALLOWED_HOSTS="*"

# Restart Django server
echo "🔄 Restarting Django..."
pkill -f "python manage.py runserver"
sleep 2

# Start Django with explicit ALLOWED_HOSTS
ALLOWED_HOSTS="*" python manage.py runserver 0.0.0.0:8000 &

echo "✅ Django restarted with ALLOWED_HOSTS=*"
echo "🔍 Check logs: tail -f logs/django.log"
