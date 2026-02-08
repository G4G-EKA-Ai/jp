#!/bin/bash
# Update Emergent deployment to use JPFINAL repo

cd /app

# Backup current deployment
echo "📦 Backing up current deployment..."
cp -r /app /tmp/app_backup_$(date +%Y%m%d_%H%M%S)

# Remove old files (keep db.sqlite3 and logs)
echo "🗑️ Removing old files..."
find /app -mindepth 1 -maxdepth 1 ! -name 'db.sqlite3' ! -name 'logs' ! -name 'media' -exec rm -rf {} +

# Clone new repo
echo "📥 Cloning JPFINAL repo..."
git clone https://github.com/ekaaiurgaa-glitch/JPFINAL.git /tmp/jpfinal
cd /tmp/jpfinal

# Move files to /app
echo "📂 Moving files to /app..."
mv /tmp/jpfinal/* /app/
mv /tmp/jpfinal/.* /app/ 2>/dev/null || true

# Cleanup
rm -rf /tmp/jpfinal

# Install dependencies
echo "📦 Installing dependencies..."
cd /app
pip install --no-cache-dir -r backend/requirements.txt

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create initial user if needed
echo "👤 Creating initial user..."
python manage.py create_initial_user

echo "✅ Deployment updated to JPFINAL repo"
echo "🔄 Restart the service to apply changes"
