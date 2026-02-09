#!/usr/bin/env python
"""
SQLite to PostgreSQL Data Export Script for JAYTI
Exports all user data from SQLite database to JSON files for migration.

Usage:
    python scripts/export_sqlite_data.py

Output:
    Creates JSON files in /app/data_export/ directory
"""
import os
import sys
import json
from datetime import datetime

# Setup Django
sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaytipargal.settings')

import django
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, DailyThought, PushSubscription, NotificationSchedule
from notes.models import Note, NoteFolder
from diary.models import DiaryEntry
from goals.models import Goal, Task
from ai_chat.models import AIConversation, AIMessage

# Create export directory
EXPORT_DIR = '/app/data_export'
os.makedirs(EXPORT_DIR, exist_ok=True)

def serialize_datetime(obj):
    """JSON serializer for datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def export_users():
    """Export users and profiles"""
    print("Exporting users...")
    users_data = []
    for user in User.objects.all():
        user_dict = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined.isoformat() if user.date_joined else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            # Note: Password hash is exported for migration
            'password': user.password,
        }
        
        # Export profile if exists
        try:
            profile = user.profile
            user_dict['profile'] = {
                'display_name': profile.display_name,
                'preferred_language': profile.preferred_language,
                'birthday_message_seen_2026': profile.birthday_message_seen_2026,
                'created_at': profile.created_at.isoformat() if profile.created_at else None,
            }
        except UserProfile.DoesNotExist:
            user_dict['profile'] = None
            
        users_data.append(user_dict)
    
    with open(f'{EXPORT_DIR}/users.json', 'w') as f:
        json.dump(users_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(users_data)} users")
    return len(users_data)

def export_notes():
    """Export notes and folders"""
    print("Exporting notes...")
    
    # Export folders first
    folders_data = []
    for folder in NoteFolder.objects.all():
        folders_data.append({
            'id': folder.id,
            'user_id': folder.user_id,
            'name': folder.name,
            'color': folder.color,
            'created_at': folder.created_at.isoformat() if folder.created_at else None,
        })
    
    with open(f'{EXPORT_DIR}/note_folders.json', 'w') as f:
        json.dump(folders_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(folders_data)} folders")
    
    # Export notes
    notes_data = []
    for note in Note.objects.all():
        notes_data.append({
            'id': note.id,
            'user_id': note.user_id,
            'folder_id': note.folder_id,
            'title': note.title,
            'content': note.content,
            'is_pinned': note.is_pinned,
            'created_at': note.created_at.isoformat() if note.created_at else None,
            'updated_at': note.updated_at.isoformat() if note.updated_at else None,
        })
    
    with open(f'{EXPORT_DIR}/notes.json', 'w') as f:
        json.dump(notes_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(notes_data)} notes")
    return len(notes_data)

def export_diary():
    """Export diary entries"""
    print("Exporting diary...")
    
    # Export diary entries
    diary_data = []
    for entry in DiaryEntry.objects.all():
        diary_data.append({
            'id': entry.id,
            'user_id': entry.user_id,
            'title': entry.title,
            'content': entry.content,
            'mood': entry.mood,
            'mood_intensity': entry.mood_intensity,
            'tags': entry.tags,
            'is_favorite': entry.is_favorite,
            'word_count': entry.word_count,
            'created_at': entry.created_at.isoformat() if entry.created_at else None,
            'updated_at': entry.updated_at.isoformat() if entry.updated_at else None,
        })
    
    with open(f'{EXPORT_DIR}/diary_entries.json', 'w') as f:
        json.dump(diary_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(diary_data)} diary entries")
    return len(diary_data)

def export_goals():
    """Export goals and tasks"""
    print("Exporting goals...")
    
    goals_data = []
    for goal in Goal.objects.all():
        goals_data.append({
            'id': goal.id,
            'user_id': goal.user_id,
            'title': goal.title,
            'description': goal.description,
            'category': goal.category,
            'priority': goal.priority,
            'status': goal.status,
            'target_date': goal.target_date.isoformat() if goal.target_date else None,
            'created_at': goal.created_at.isoformat() if goal.created_at else None,
            'updated_at': goal.updated_at.isoformat() if goal.updated_at else None,
        })
    
    with open(f'{EXPORT_DIR}/goals.json', 'w') as f:
        json.dump(goals_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(goals_data)} goals")
    
    # Export tasks
    tasks_data = []
    for task in Task.objects.all():
        tasks_data.append({
            'id': task.id,
            'goal_id': task.goal_id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'created_at': task.created_at.isoformat() if task.created_at else None,
        })
    
    with open(f'{EXPORT_DIR}/tasks.json', 'w') as f:
        json.dump(tasks_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(tasks_data)} tasks")
    return len(goals_data)

def export_ai_chat():
    """Export AI chat sessions and messages"""
    print("Exporting AI chat...")
    
    sessions_data = []
    for session in ChatSession.objects.all():
        sessions_data.append({
            'id': session.id,
            'user_id': session.user_id,
            'title': session.title,
            'created_at': session.created_at.isoformat() if session.created_at else None,
            'updated_at': session.updated_at.isoformat() if session.updated_at else None,
        })
    
    with open(f'{EXPORT_DIR}/chat_sessions.json', 'w') as f:
        json.dump(sessions_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(sessions_data)} chat sessions")
    
    messages_data = []
    for msg in ChatMessage.objects.all():
        messages_data.append({
            'id': msg.id,
            'session_id': msg.session_id,
            'role': msg.role,
            'content': msg.content,
            'created_at': msg.created_at.isoformat() if msg.created_at else None,
        })
    
    with open(f'{EXPORT_DIR}/chat_messages.json', 'w') as f:
        json.dump(messages_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(messages_data)} chat messages")
    return len(sessions_data)

def export_daily_thoughts():
    """Export daily thoughts"""
    print("Exporting daily thoughts...")
    
    thoughts_data = []
    for thought in DailyThought.objects.all():
        thoughts_data.append({
            'id': thought.id,
            'content': thought.content,
            'author': thought.author,
            'category': thought.category,
            'is_active': thought.is_active,
            'created_at': thought.created_at.isoformat() if thought.created_at else None,
        })
    
    with open(f'{EXPORT_DIR}/daily_thoughts.json', 'w') as f:
        json.dump(thoughts_data, f, indent=2, default=serialize_datetime)
    print(f"  Exported {len(thoughts_data)} daily thoughts")
    return len(thoughts_data)

def main():
    print("=" * 50)
    print("JAYTI SQLite Data Export")
    print("=" * 50)
    print(f"Export directory: {EXPORT_DIR}")
    print()
    
    total = 0
    total += export_users()
    total += export_notes()
    total += export_diary()
    total += export_goals()
    total += export_ai_chat()
    total += export_daily_thoughts()
    
    print()
    print("=" * 50)
    print(f"Export complete! Total records: {total}")
    print(f"Files saved to: {EXPORT_DIR}/")
    print("=" * 50)
    
    # List exported files
    print("\nExported files:")
    for f in sorted(os.listdir(EXPORT_DIR)):
        size = os.path.getsize(f'{EXPORT_DIR}/{f}')
        print(f"  - {f} ({size} bytes)")

if __name__ == '__main__':
    main()
