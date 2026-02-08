# JAYTI - Personal Life Companion Website

## Project Overview
A personal, feature-rich website created as a birthday gift for Jayti. Built with Django 4.2 + Python 3.11, featuring Vedic Astrology, AI Chat, Notes, Diary, and Goals management.

## Current Status: ✅ DEPLOYED & RUNNING
- **Preview URL:** https://ai-companion-app-30.preview.emergentagent.com/
- **Last Updated:** February 8, 2026
- **Database:** SQLite (local file)

## Core Features (Implemented)
1. ✅ **Dashboard** - Main hub with Karma, Dharma, Doubt, Memory, Thoughts cards
2. ✅ **Birthday Countdown Widget** - Shows days until Feb 6, with special celebration on birthday
3. ✅ **Notes** - Create, edit, pin notes with tags
4. ✅ **Diary** - Journal entries with mood tracking
5. ✅ **Goals** - Goal tracking with Kanban board and progress charts
6. ✅ **Vedic Astrology** - Birth chart with Whole Sign Houses, Dasha periods, 12 Houses
7. ✅ **AI Chat (Ask Jayti)** - Gemini 1.5 Pro integration
8. ✅ **Health Check** - `/health/` endpoint for deployment verification

## Login Credentials
- **Username:** jayati
- **Password:** jayati2026

## Environment Configuration
- **GEMINI_API_KEY:** Configured
- **Database:** SQLite (db.sqlite3)
- **Static Files:** WhiteNoise for serving

## Tech Stack
- Django 4.2
- Python 3.11
- SQLite Database
- Gemini 1.5 Pro (AI)
- Swiss Ephemeris (Astrology)
- Chart.js (Data visualization)
- WhiteNoise (Static files)

## Key Files
- `/app/jaytipargal/settings.py` - Main configuration
- `/app/backend/.env` - Environment variables
- `/app/core/views.py` - Dashboard, birthday countdown & auth views
- `/app/astro/views.py` - Vedic astrology calculations
- `/app/templates/core/dashboard.html` - Dashboard with birthday widget

## Future Enhancements (Backlog)
- P1: Note Folders
- P1: PDF Export for Notes/Diary
- P1: Dark Mode toggle
- P1: Full PWA with offline support
- P2: Push Notifications
- P2: Daily Briefing & Weekly Summary
- P2: PostgreSQL migration for production
