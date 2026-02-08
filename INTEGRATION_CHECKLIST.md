# QUICK INTEGRATION CHECKLIST
# Copy-paste these code snippets into existing files

## 1. UPDATE core/models.py (ADD TO END OF FILE)

```python
# Import notification models
from core.models_notifications import PushSubscription, NotificationSchedule
```

## 2. UPDATE notes/models.py (ADD TO END OF FILE)

```python
# Import folder model
from notes.models_folders import NoteFolder

# Add this field to Note model (via migration):
# folder = models.ForeignKey(NoteFolder, null=True, blank=True, on_delete=models.SET_NULL, related_name='notes')
```

## 3. UPDATE jaytipargal/urls.py (REPLACE ENTIRE FILE)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from core.api_urls import api_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('notes/', include('notes.urls')),
    path('diary/', include('diary.urls')),
    path('goals/', include('goals.urls')),
    path('astro/', include('astro.urls')),
    path('ai-chat/', include('ai_chat.urls')),
    path('manifest.json', TemplateView.as_view(
        template_name='manifest.json',
        content_type='application/json'
    )),
] + api_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## 4. UPDATE jaytipargal/settings.py (ADD TO END OF FILE)

```python
# VAPID keys for web push notifications
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', '')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', '')
VAPID_ADMIN_EMAIL = os.environ.get('VAPID_ADMIN_EMAIL', 'admin@jaytibirthday.in')

# SSL/HTTPS settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

## 5. UPDATE templates/base.html (ADD TO <head>)

```html
<!-- PWA and Dark Mode -->
<link rel="manifest" href="{% static 'manifest.json' %}">
<link rel="stylesheet" href="{% static 'css/dark-mode.css' %}">
<meta name="theme-color" content="#FF69B4">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="{% static 'icons/icon-192x192.png' %}">
```

## 6. UPDATE templates/base.html (ADD BEFORE </body>)

```html
<!-- Dark Mode and PWA Scripts -->
<script src="{% static 'js/dark-mode.js' %}"></script>
<script src="{% static 'js/pwa-register.js' %}"></script>
```

## 7. UPDATE core/views.py dashboard() FUNCTION

```python
@login_required
def dashboard(request):
    from notes.models import Note
    from diary.models import DiaryEntry
    from goals.models import Goal, Task
    from datetime import datetime
    from django.utils import timezone
    import pytz
    
    recent_notes = Note.objects.filter(user=request.user).count()
    recent_diary = DiaryEntry.objects.filter(user=request.user).count()
    active_goals = Goal.objects.filter(user=request.user, status='active').count()
    pending_tasks = Task.objects.filter(goal__user=request.user, status='pending').count()
    
    now_utc = timezone.now()
    ist_tz = pytz.timezone('Asia/Kolkata')
    today_ist = now_utc.astimezone(ist_tz)
    
    is_birthday = (today_ist.month == 2 and today_ist.day == 6)
    jayti_age = today_ist.year - 1997
    show_vivek_message = is_birthday
    show_weekly_summary = (today_ist.weekday() == 6)  # Sunday
    
    context = {
        'recent_notes': recent_notes,
        'recent_diary': recent_diary,
        'active_goals': active_goals,
        'pending_tasks': pending_tasks,
        'show_vivek_message': show_vivek_message,
        'is_birthday': is_birthday,
        'jayti_age': jayti_age,
        'show_weekly_summary': show_weekly_summary,
    }
    
    return render(request, 'core/dashboard_enhanced.html', context)
```

## 8. UPDATE backend/requirements.txt (REPLACE ENTIRE FILE)

```
Django>=4.2,<5.0
dj-database-url>=2.0.0
whitenoise>=6.5.0
python-dotenv>=1.0.0
pytz>=2023.3
gunicorn>=21.0.0
psycopg2-binary>=2.9.0
Pillow>=10.0.0
pyswisseph>=2.10.0
google-genai>=1.0.0
uvicorn>=0.29.0
reportlab>=4.0.0
pywebpush>=1.14.0
```

## 9. UPDATE backend/.env (ADD THESE VARIABLES)

```bash
# VAPID Keys (generate with: python -c "from pywebpush import webpush; vapid = webpush.WebPushVAPID(); vapid.generate_keys(); print(vapid.private_key.decode()); print(vapid.public_key.decode())")
VAPID_PRIVATE_KEY=your_generated_private_key_here
VAPID_PUBLIC_KEY=your_generated_public_key_here
VAPID_ADMIN_EMAIL=admin@jaytibirthday.in

# PostgreSQL Database (from Neon.tech, Supabase, or CockroachDB)
DATABASE_URL=postgresql://user:password@host:5432/database
```

## 10. UPDATE static/js/pwa-register.js (REPLACE VAPID KEY)

```javascript
// At the bottom of the file, replace:
const VAPID_PUBLIC_KEY = 'YOUR_VAPID_PUBLIC_KEY_HERE';

// With your actual public key from backend/.env
const VAPID_PUBLIC_KEY = 'your_actual_vapid_public_key';
```

## 11. RUN THESE COMMANDS IN ORDER

```bash
# Install new dependencies
pip install -r backend/requirements.txt

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create seed content
python manage.py seed_content

# Collect static files
python manage.py collectstatic --noinput

# Test the server
python manage.py runserver
```

## 12. VERIFY FEATURES WORK

Open browser and test:
- [ ] http://localhost:8001/ - Dashboard loads with briefing
- [ ] http://localhost:8001/api/daily-briefing/ - Returns JSON
- [ ] http://localhost:8001/api/mood-trends/ - Returns chart data
- [ ] http://localhost:8001/api/goal-progress/ - Returns chart data
- [ ] Dark mode toggle button appears (bottom right)
- [ ] PWA install prompt appears (bottom left)
- [ ] Charts display on dashboard
- [ ] Notification permission prompt appears

## 13. DEPLOY TO PRODUCTION

```bash
# Push to Railway/Emergent
git add .
git commit -m "Add all enhanced features: PWA, AI briefing, charts, dark mode, notifications"
git push origin main

# Set environment variables on Railway:
# - DATABASE_URL (from Neon.tech/Supabase)
# - VAPID_PRIVATE_KEY
# - VAPID_PUBLIC_KEY
# - GEMINI_API_KEY

# Run migrations on production
railway run python manage.py migrate
railway run python manage.py seed_content
railway run python manage.py collectstatic --noinput
```

## 14. SETUP CRON JOBS (Railway)

Add to railway.json or use Railway's cron feature:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn jaytipargal.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  },
  "cron": [
    {
      "schedule": "*/5 * * * *",
      "command": "python manage.py send_notifications"
    },
    {
      "schedule": "0 2 * * *",
      "command": "python manage.py backup_database"
    }
  ]
}
```

## 15. FINAL VERIFICATION

Test on mobile device:
- [ ] Visit https://your-domain.com
- [ ] Click "Add to Home Screen"
- [ ] Open app from home screen
- [ ] Enable notifications
- [ ] Toggle dark mode
- [ ] View charts on dashboard
- [ ] Search diary entries
- [ ] Export diary to PDF

---

## 🎉 DONE!

All features are now integrated. The website is production-ready with:
- PWA support
- AI-powered insights
- Visual analytics
- Push notifications
- Dark mode
- PDF export
- Full-text search
- Automated backups

**Enjoy your enhanced personal companion! 💖**
