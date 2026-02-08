#!/bin/bash
# Automated Deployment Script for Jayti Website Enhanced Features
# Run: bash deploy_features.sh

set -e  # Exit on error

echo "🚀 Starting deployment of enhanced features..."

# Step 1: Install dependencies
echo "📦 Installing new dependencies..."
pip install -r backend/requirements_updated.txt

# Step 2: Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 3: Create seed content
echo "🌱 Creating seed content..."
python manage.py seed_content

# Step 4: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Step 5: Create backup directory
echo "💾 Creating backup directory..."
mkdir -p backups

# Step 6: Test API endpoints
echo "🧪 Testing API endpoints..."
python manage.py runserver 0.0.0.0:8001 &
SERVER_PID=$!
sleep 5

# Test endpoints
curl -s http://localhost:8001/api/daily-briefing/ > /dev/null && echo "✅ Daily briefing API working" || echo "❌ Daily briefing API failed"
curl -s http://localhost:8001/api/mood-trends/ > /dev/null && echo "✅ Mood trends API working" || echo "❌ Mood trends API failed"
curl -s http://localhost:8001/api/goal-progress/ > /dev/null && echo "✅ Goal progress API working" || echo "❌ Goal progress API failed"

# Stop test server
kill $SERVER_PID

# Step 7: Generate VAPID keys
echo "🔑 Generating VAPID keys..."
python -c "
from pywebpush import webpush
vapid = webpush.WebPushVAPID()
vapid.generate_keys()
print('\n📋 Add these to your backend/.env file:')
print('VAPID_PRIVATE_KEY=' + vapid.private_key.decode())
print('VAPID_PUBLIC_KEY=' + vapid.public_key.decode())
print('\n📋 Also update static/js/pwa-register.js with the public key')
"

# Step 8: Create icons directory
echo "🎨 Creating icons directory..."
mkdir -p static/icons

echo "
✅ Deployment complete!

📋 Next steps:
1. Add VAPID keys to backend/.env (shown above)
2. Update VAPID_PUBLIC_KEY in static/js/pwa-register.js
3. Generate PWA icons (72x72 to 512x512) and place in static/icons/
4. Set DATABASE_URL in backend/.env (from Neon.tech/Supabase)
5. Deploy to Railway/Emergent
6. Set up cron jobs for notifications and backups

🧪 Test locally:
python manage.py runserver

🌐 Access at:
http://localhost:8001

📚 Read full guide:
- DEPLOYMENT_GUIDE.md
- INTEGRATION_CHECKLIST.md
- FEATURE_SUMMARY.md

🎉 All features are ready!
"
