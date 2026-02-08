# JAYTI Birthday Website - PRD

## Project Overview
Personal life companion website for Jayti Pargal, built with Django. Deployed on Emergent platform via Django ASGI (uvicorn) on port 8001 with Node.js proxy on port 3000.

## Architecture
- **Backend**: Django 4.2 ASGI via uvicorn (port 8001)
- **Frontend**: Django Templates proxied via Node.js (port 3000)
- **Database**: SQLite (file-based, no external DB dependency)
- **AI**: Google Gemini 1.5 Pro (chat + goal generation)
- **Astrology**: Swiss Ephemeris (pyswisseph)
- **Static Files**: WhiteNoise

## What's Been Implemented (All verified working - Feb 7, 2026)
1. Login Page - Daily thoughts, flower slideshow, live clock, birthday overlay (Feb 6)
2. Dashboard - Navigation hub with all 6 sections
3. Notes - CRUD with tags, search, pin support
4. Diary - Type/Voice/Handwriting input, mood tracking, calendar, streaks, daily prompts
5. Goals - AI-powered task generation, Kanban board, milestones, department breakdown
6. Astro - Vedic birth chart, 12 houses analysis, Vimshottari Dasha, 90-day predictions
7. AI Chat - Gemini-powered Mentor Mode with context awareness (goals + mood)
8. Profile - Display name, password change, profile picture upload
9. Health Check - /health/ endpoint (DB, static, astro status)

## Deployment Fixes Applied (Feb 7, 2026)
- requirements.txt cleaned: 132 packages -> 11 actual dependencies
- frontend/.env created with REACT_APP_BACKEND_URL
- backend/.env: DEBUG=False for production
- frontend/server.js: ports read from environment variables
- settings.py: removed hardcoded SECRET_KEY fallback, DEBUG defaults to False
- server.py: background thread for migrations/setup on startup
- Database: SQLite (no PostgreSQL dependency for Emergent)

## Bugs Fixed Previously
- Gemini model: gemini-pro -> gemini-1.5-pro
- google-generativeai SDK -> google-genai
- Birthday dismiss: removed @login_required
- @csrf_exempt removed from AI chat
- Astro predictions: KeyError 'house' fixed
- Birth chart: missing template filters added
- DiaryPrompt migration created
- initial_data fixture loaded

## Credentials
- Username: jayati | Password: jayati2026

## Deployment Checklist
- [x] Django ASGI on port 8001
- [x] Node.js proxy on port 3000
- [x] SQLite database (no external DB needed)
- [x] Static files via WhiteNoise
- [x] Health check at /health/
- [x] CSRF_TRUSTED_ORIGINS includes *.preview.emergentagent.com
- [x] ALLOWED_HOSTS includes Emergent domains
- [x] Migrations run on startup
- [x] Initial user created automatically
- [x] Fixture data loaded
