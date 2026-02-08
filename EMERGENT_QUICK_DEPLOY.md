# Quick Deploy Prompt for Emergent

## Action Required
Deploy the JAYTI Personal Life Companion application from the **main branch** of this repository.

---

## Repository
```
https://github.com/ekaaiurgaa-glitch/JPFINAL
Branch: main
```

---

## Recent Update
The `conflict_080226_1102` branch has been merged into `main`. All 21 features are now consolidated in the main branch, including:

1. **NEW**: Birthday Countdown Widget - shows days until Feb 6 birthday
2. **NEW**: Goals Chart Data - task counts & department distribution  
3. **NEW**: Simplified AI System Prompt - cleaner "Ask Jayti" mentor
4. **EXISTING**: Notes, Diary, Goals, Astro, AI Chat, PWA, Dark Mode, Offline support

---

## Environment Variables

Set these in Emergent Variables section:

```env
SECRET_KEY=django-insecure-jayti-emergent-2026-prod-key
DEBUG=False
ALLOWED_HOSTS=*.preview.emergentagent.com,*.emergentagent.com,localhost,127.0.0.1
GEMINI_API_KEY=AIzaSyC5F5GSfJeB1_4qN5J_X8L8Tzp9KQGgGqg
TIME_ZONE=Asia/Kolkata
```

---

## Deployment Command

Run this single command in Emergent terminal:

```bash
cd /app && bash deploy_emergent.sh
```

This will:
- Install dependencies
- Run migrations
- Create user: jayati/jayati2026
- Seed initial content
- Collect static files

---

## Start Server

```bash
cd /app/backend && gunicorn jaytipargal.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 2
```

Or simply:
```bash
cd /app && python manage.py runserver 0.0.0.0:8000
```

---

## Verification

1. Open your Emergent domain URL
2. Login with: **jayati** / **jayati2026**
3. Check dashboard shows all 6 sections
4. Test AI chat responds
5. Verify Goals page shows progress charts

---

## Health Check

```
GET /health/
```

Should return JSON with database and static files status.

---

**Deploy from MAIN branch only. The conflict branch has been deleted and merged.**
