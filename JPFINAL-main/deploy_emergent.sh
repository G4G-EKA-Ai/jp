#!/bin/bash
# Emergent Deployment Script for Jayti Website

set -e

echo "🚀 Starting Jayti deployment..."

# Install dependencies
echo "📦 Installing Python dependencies..."
python -m pip install --no-cache-dir -r backend/requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create initial user
echo "👤 Creating initial user..."
python manage.py create_initial_user

# Seed content
echo "🌱 Seeding welcome content..."
python manage.py seed_content || echo "⚠️ Seed content command not found, skipping..."

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create directories
echo "📂 Creating required directories..."
mkdir -p logs backups media

echo "✅ Deployment complete!"
echo "🌐 Access your site at your Emergent URL"
echo "🔑 Login: jayati / jayati2026"
