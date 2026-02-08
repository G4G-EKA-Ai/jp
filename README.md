# 💝 JAYTI - Personal Life Companion

A beautiful, feature-rich personal companion website built with love as a birthday gift.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![AI](https://img.shields.io/badge/AI-Gemini%201.5%20Pro-purple)

## ✨ Features

### 📝 Notes
- Create, edit, and organize notes with folders
- Tag system for easy categorization
- Pin important notes
- Search functionality
- Export to PDF

### 📔 Diary
- Daily journal entries
- Multiple input modes: Type, Voice, Handwrite
- Mood tracking with visualizations
- Daily reflection prompts
- Export to PDF

### 🎯 Goals
- AI-powered goal planning
- Kanban board for task management
- Progress tracking with charts
- Department-wise task breakdown
- Marketing career roadmap

### 🔮 Vedic Astrology
- Complete birth chart (Kundli)
- 12 House analysis
- Dasha periods & predictions
- Daily cosmic guidance

### 🤖 Ask Jayti (AI Companion)
- Personal AI mentor powered by Gemini
- Contextual conversations
- Quick actions for goals, mood, motivation
- Private and secure

### 🎂 Special Features
- Birthday countdown widget
- Dark mode toggle
- PWA support (installable)
- Responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jayti.git
cd jayti

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your GEMINI_API_KEY

# Run migrations
python manage.py migrate

# Create initial user
python manage.py create_initial_user

# Collect static files
python manage.py collectstatic --noinput

# Start the server
python manage.py runserver
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI features | Yes |
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (False in production) | No |
| `ALLOWED_HOSTS` | Allowed host domains | Yes |

## 📁 Project Structure

```
jayti/
├── core/           # Authentication, dashboard, profile
├── notes/          # Notes module
├── diary/          # Diary module
├── goals/          # Goals & tasks module
├── astro/          # Vedic astrology module
├── ai_chat/        # AI companion module
├── templates/      # HTML templates
├── static/         # CSS, JS, images
├── docs/           # Documentation
└── manage.py
```

## 🛠️ Tech Stack

- **Backend:** Django 4.2, Python 3.11
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **AI:** Google Gemini 1.5 Pro
- **Astrology:** Swiss Ephemeris (pyswisseph)
- **Frontend:** Django Templates, Bootstrap 5, Chart.js
- **Server:** Gunicorn, WhiteNoise

## 📖 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Feature Summary](docs/FEATURE_SUMMARY.md)

## 🔐 Default Credentials

- **Username:** jayati
- **Password:** jayati2026

## 📄 License

This project is a personal gift and is not licensed for redistribution.

---

Made with 💕 for Jayti
