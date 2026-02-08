# JAYTI - Personal Life Companion

A deeply personal, secure website built as a birthday gift for Jayti Pargal. Organizes thoughts, plans goals, tracks progress, and provides guidance.

## Features

| Section | Description |
|---------|-------------|
| **Notes** | Day-wise notes with tags, search, and pin support |
| **Diary** | Typing, voice-to-text, and handwriting input with mood tracking |
| **Goals** | AI-powered marketing career roadmap with Kanban board |
| **Astro** | Vedic birth chart, 12 houses, Dasha periods, 90-day guidance |
| **Ask Jayti** | Gemini-powered AI companion with Mentor Mode |
| **Profile** | Display name, password change, profile picture |

## Tech Stack

- **Framework**: Django 4.2 (ASGI)
- **Database**: SQLite (default) / PostgreSQL (production)
- **AI**: Google Gemini 1.5 Pro
- **Astrology**: Swiss Ephemeris (pyswisseph)
- **Static Files**: WhiteNoise
- **Server**: Uvicorn (ASGI)

## Project Structure

```
/app/
├── jaytipargal/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/                 # Auth, profile, dashboard
├── notes/                # Notes app
├── diary/                # Diary app (type/voice/write)
├── goals/                # Goal tracking app
├── astro/                # Vedic astrology app
├── ai_chat/              # AI chatbot app
├── templates/            # Django HTML templates
│   ├── base.html
│   ├── core/
│   ├── notes/
│   ├── diary/
│   ├── goals/
│   ├── astro/
│   └── ai_chat/
├── static/               # CSS, JS, images
├── backend/              # Emergent platform wrapper
│   ├── server.py         # Django ASGI entry point
│   ├── .env              # Environment variables
│   └── requirements.txt  # Python dependencies
├── frontend/             # Emergent platform proxy
│   ├── server.js         # Node.js proxy to Django
│   ├── package.json
│   └── .env
├── manage.py
└── README.md
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | No | Default: False |
| `ALLOWED_HOSTS` | Yes | Comma-separated hostnames |
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `GEMINI_MODEL` | No | Default: gemini-1.5-pro |
| `DATABASE_URL` | No | PostgreSQL URL (falls back to SQLite) |
| `TIME_ZONE` | No | Default: Asia/Kolkata |
| `BIRTH_DATE_DAY` | No | Default: 6 |
| `BIRTH_DATE_MONTH` | No | Default: 2 |

## Setup

```bash
pip install -r backend/requirements.txt
python manage.py migrate
python manage.py create_initial_user
python manage.py collectstatic --noinput
python manage.py loaddata initial_data
```

## Credentials

- **Username**: jayati
- **Password**: jayati2026

---
*Created with love for Jayti Pargal's birthday - February 6, 2026*
