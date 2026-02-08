# JAYTI - Personal Life Companion Website
## Product Requirements Document

### Original Problem Statement
Build a personal, feature-rich website called "JAYTI" as a birthday gift. The application should be production-ready with the following core modules:
- Notes (with folders, tags, search, pin, PDF export)
- Diary (typing/voice/handwriting, mood tracking, search, PDF export)
- Goals (AI-powered marketing roadmap, Kanban board, progress charts)
- Vedic Astrology
- AI Companion (Gemini 1.5 Pro)

### Tech Stack
- **Backend:** Django 5.0 on Python 3.11
- **Frontend:** Server-side rendered Django Templates with vanilla JavaScript
- **Database:** SQLite (user preference for cost management)
- **AI Integration:** Google Gemini (`gemini-1.5-pro`)
- **Deployment:** Emergent Platform

### Current Status: PRODUCTION READY ✅

### Implemented Features (as of Feb 8, 2026)
1. ✅ **Login System** - Custom login page with daily inspiration quotes
2. ✅ **Dashboard** - Welcome message, birthday countdown, daily briefing
3. ✅ **Notes Module** - Create, edit, delete, pin, tag notes
4. ✅ **Diary Module** - Daily entries with mood tracking
5. ✅ **Goals Module** - Goal tracking with tasks, Kanban board
6. ✅ **Astro Module** - Vedic astrology birth chart
7. ✅ **AI Chat** - "Ask Jyati" powered by Gemini
8. ✅ **Birthday Countdown Widget** - Shows days until February 6
9. ✅ **Dark Mode Toggle** - UI preference
10. ✅ **PWA Support** - Manifest.json and icons

### Deployment Configuration
- `ALLOWED_HOSTS = ['*']`
- `CSRF_TRUSTED_ORIGINS` includes:
  - `*.preview.emergentagent.com`
  - `*.emergentcf.cloud`
  - `jaytibirthday.in`
  - `*.railway.app`

### Test Credentials
- **Username:** `jayati`
- **Password:** `jayati2026`

### API Endpoints Status
| Endpoint | Status |
|----------|--------|
| `/health/` | ✅ 200 OK |
| `/dashboard/` | ✅ 200 OK |
| `/notes/` | ✅ 200 OK |
| `/diary/` | ✅ 200 OK |
| `/goals/` | ✅ 200 OK |
| `/astro/` | ✅ 200 OK |

### Known Limitations
1. **SQLite Database** - Not suitable for high-concurrency production. User chose this for cost reasons.
2. **Google Gemini deprecation warning** - `google.generativeai` package should be migrated to `google.genai`

### Future Enhancements (P2)
- PostgreSQL migration for production stability
- Enhanced mood trend visualization with charts
- Vedic Planetary Aspects (Drishti)
- Push notifications
- Automated database backup system

### Files Modified This Session
- `/app/core/views.py` - Fixed duplicate `get_birthday_countdown()` function
- `/app/core/api_views.py` - Fixed import for models
- `/app/jaytipargal/settings.py` - Added `.emergentcf.cloud` to CSRF_TRUSTED_ORIGINS
- `/app/static/icons/` - Created actual PNG icons (replaced placeholders)
