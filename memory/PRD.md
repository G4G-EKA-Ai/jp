# JAYTI Birthday Website - PRD

## Project Overview
Personal life companion website for Jayti Pargal, built with Django. Deployed on Emergent platform via Django ASGI (uvicorn) on port 8001 with Node.js proxy on port 3000.

## Architecture
- **Backend**: Django 4.2 ASGI via uvicorn (port 8001)
- **Frontend**: Django Templates proxied via Node.js (port 3000)
- **Database**: SQLite (local), PostgreSQL-ready via dj-database-url
- **AI**: Google Gemini 1.5 Pro (chat + goal generation)
- **Astrology**: Swiss Ephemeris (pyswisseph)
- **Static Files**: WhiteNoise

## What's Been Implemented (All verified working - Feb 7, 2026)
1. **Login Page** - Daily thoughts, flower slideshow, live clock, birthday overlay (Feb 6)
2. **Dashboard** - Navigation hub with all 6 sections
3. **Notes** - CRUD with tags, search, pin support
4. **Diary** - Type/Voice/Handwriting input, mood tracking, calendar, streaks, daily prompts
5. **Goals** - AI-powered task generation, Kanban board, milestones, department breakdown
6. **Astro** - Vedic birth chart, 12 houses analysis, Vimshottari Dasha, 90-day predictions
7. **AI Chat** - Gemini-powered Mentor Mode with context awareness (goals + mood)
8. **Profile** - Display name, password change, profile picture upload
9. **Health Check** - /health/ endpoint (DB, static, astro status)

## Bugs Fixed
- Gemini model updated: `gemini-pro` -> `gemini-1.5-pro` (deprecated)
- google-generativeai SDK -> google-genai (new SDK)
- Birthday dismiss endpoint: removed @login_required
- @csrf_exempt removed from AI chat (security fix)
- Astro predictions: KeyError 'house' fixed with .get() defaults
- Birth chart: Added missing `month_name` and `format_minute` template filters
- Missing DiaryPrompt migration created
- initial_data fixture loaded

## Credentials
- Username: jayati | Password: jayati2026

## Backlog (P1)
- Visual progress charts in Goals (Chart.js)
- Goal analytics dashboard
- Task reminder notifications

## Backlog (P2)
- Vedic planetary aspects (drishti) calculation
- Separate "Things to Avoid" / "Areas to Focus" in Astro
- Monthly breakdown in predictions
