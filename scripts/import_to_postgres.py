#!/usr/bin/env python
"""
PostgreSQL Data Import Script for JAYTI
Imports data from JSON export files into PostgreSQL database.

Usage:
    1. Set DATABASE_URL environment variable to your Supabase PostgreSQL URL
    2. Run: python scripts/import_to_postgres.py

Prerequisites:
    - Export data first using export_sqlite_data.py
    - PostgreSQL database must be empty (migrations applied)
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

from django.db import transaction
from django.contrib.auth.models import User
from core.models import UserProfile, DailyThought
from notes.models import Note, NoteFolder
from diary.models import DiaryEntry
from goals.models import Goal, Task
from ai_chat.models import AIConversation, AIMessage

EXPORT_DIR = '/app/data_export'

def parse_datetime(dt_str):
    """Parse ISO datetime string"""
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return None

def import_users():
    """Import users and profiles"""
    filepath = f'{EXPORT_DIR}/users.json'
    if not os.path.exists(filepath):
        print("  No users.json found, skipping...")
        return 0
    
    print("Importing users...")
    with open(filepath, 'r') as f:
        users_data = json.load(f)
    
    count = 0
    for user_dict in users_data:
        # Check if user already exists
        if User.objects.filter(username=user_dict['username']).exists():
            print(f"  User '{user_dict['username']}' already exists, skipping...")
            continue
        
        user = User(
            id=user_dict['id'],
            username=user_dict['username'],
            email=user_dict['email'],
            first_name=user_dict['first_name'],
            last_name=user_dict['last_name'],
            is_active=user_dict['is_active'],
            is_staff=user_dict['is_staff'],
            is_superuser=user_dict['is_superuser'],
            password=user_dict['password'],  # Already hashed
        )
        if user_dict['date_joined']:
            user.date_joined = parse_datetime(user_dict['date_joined'])
        if user_dict['last_login']:
            user.last_login = parse_datetime(user_dict['last_login'])
        user.save()
        
        # Create profile
        if user_dict.get('profile'):
            profile_data = user_dict['profile']
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'display_name': profile_data.get('display_name', ''),
                    'preferred_language': profile_data.get('preferred_language', 'en'),
                    'birthday_message_seen_2026': profile_data.get('birthday_message_seen_2026', False),
                }
            )
        
        count += 1
    
    print(f"  Imported {count} users")
    return count

def import_note_folders():
    """Import note folders"""
    filepath = f'{EXPORT_DIR}/note_folders.json'
    if not os.path.exists(filepath):
        print("  No note_folders.json found, skipping...")
        return 0
    
    print("Importing note folders...")
    with open(filepath, 'r') as f:
        folders_data = json.load(f)
    
    count = 0
    for folder_dict in folders_data:
        NoteFolder.objects.update_or_create(
            id=folder_dict['id'],
            defaults={
                'user_id': folder_dict['user_id'],
                'name': folder_dict['name'],
                'color': folder_dict.get('color', '#6366f1'),
            }
        )
        count += 1
    
    print(f"  Imported {count} folders")
    return count

def import_notes():
    """Import notes"""
    filepath = f'{EXPORT_DIR}/notes.json'
    if not os.path.exists(filepath):
        print("  No notes.json found, skipping...")
        return 0
    
    print("Importing notes...")
    with open(filepath, 'r') as f:
        notes_data = json.load(f)
    
    count = 0
    for note_dict in notes_data:
        Note.objects.update_or_create(
            id=note_dict['id'],
            defaults={
                'user_id': note_dict['user_id'],
                'folder_id': note_dict.get('folder_id'),
                'title': note_dict['title'],
                'content': note_dict['content'],
                'is_pinned': note_dict.get('is_pinned', False),
            }
        )
        count += 1
    
    print(f"  Imported {count} notes")
    return count

def import_diary_entries():
    """Import diary entries"""
    filepath = f'{EXPORT_DIR}/diary_entries.json'
    if not os.path.exists(filepath):
        print("  No diary_entries.json found, skipping...")
        return 0
    
    print("Importing diary entries...")
    with open(filepath, 'r') as f:
        diary_data = json.load(f)
    
    count = 0
    for entry_dict in diary_data:
        DiaryEntry.objects.update_or_create(
            id=entry_dict['id'],
            defaults={
                'user_id': entry_dict['user_id'],
                'title': entry_dict.get('title', ''),
                'content': entry_dict['content'],
                'mood': entry_dict.get('mood', ''),
                'mood_intensity': entry_dict.get('mood_intensity', 5),
                'tags': entry_dict.get('tags', ''),
                'is_favorite': entry_dict.get('is_favorite', False),
                'word_count': entry_dict.get('word_count', 0),
            }
        )
        count += 1
    
    print(f"  Imported {count} diary entries")
    return count

def import_goals():
    """Import goals"""
    filepath = f'{EXPORT_DIR}/goals.json'
    if not os.path.exists(filepath):
        print("  No goals.json found, skipping...")
        return 0
    
    print("Importing goals...")
    with open(filepath, 'r') as f:
        goals_data = json.load(f)
    
    count = 0
    for goal_dict in goals_data:
        Goal.objects.update_or_create(
            id=goal_dict['id'],
            defaults={
                'user_id': goal_dict['user_id'],
                'title': goal_dict['title'],
                'description': goal_dict.get('description', ''),
                'category': goal_dict.get('category', 'personal'),
                'priority': goal_dict.get('priority', 'medium'),
                'status': goal_dict.get('status', 'active'),
                'target_date': parse_datetime(goal_dict.get('target_date')),
            }
        )
        count += 1
    
    print(f"  Imported {count} goals")
    return count

def import_tasks():
    """Import tasks"""
    filepath = f'{EXPORT_DIR}/tasks.json'
    if not os.path.exists(filepath):
        print("  No tasks.json found, skipping...")
        return 0
    
    print("Importing tasks...")
    with open(filepath, 'r') as f:
        tasks_data = json.load(f)
    
    count = 0
    for task_dict in tasks_data:
        Task.objects.update_or_create(
            id=task_dict['id'],
            defaults={
                'goal_id': task_dict['goal_id'],
                'title': task_dict['title'],
                'description': task_dict.get('description', ''),
                'status': task_dict.get('status', 'pending'),
                'priority': task_dict.get('priority', 'medium'),
                'due_date': parse_datetime(task_dict.get('due_date')),
                'completed_at': parse_datetime(task_dict.get('completed_at')),
            }
        )
        count += 1
    
    print(f"  Imported {count} tasks")
    return count

def import_chat_sessions():
    """Import AI chat sessions"""
    filepath = f'{EXPORT_DIR}/chat_sessions.json'
    if not os.path.exists(filepath):
        print("  No chat_sessions.json found, skipping...")
        return 0
    
    print("Importing chat sessions...")
    with open(filepath, 'r') as f:
        sessions_data = json.load(f)
    
    count = 0
    for session_dict in sessions_data:
        AIConversation.objects.update_or_create(
            id=session_dict['id'],
            defaults={
                'user_id': session_dict['user_id'],
                'title': session_dict.get('title', 'Chat'),
            }
        )
        count += 1
    
    print(f"  Imported {count} chat sessions")
    return count

def import_chat_messages():
    """Import AI chat messages"""
    filepath = f'{EXPORT_DIR}/chat_messages.json'
    if not os.path.exists(filepath):
        print("  No chat_messages.json found, skipping...")
        return 0
    
    print("Importing chat messages...")
    with open(filepath, 'r') as f:
        messages_data = json.load(f)
    
    count = 0
    for msg_dict in messages_data:
        AIMessage.objects.update_or_create(
            id=msg_dict['id'],
            defaults={
                'conversation_id': msg_dict.get('conversation_id') or msg_dict.get('session_id'),
                'role': msg_dict['role'],
                'content': msg_dict['content'],
            }
        )
        count += 1
    
    print(f"  Imported {count} chat messages")
    return count

def import_daily_thoughts():
    """Import daily thoughts"""
    filepath = f'{EXPORT_DIR}/daily_thoughts.json'
    if not os.path.exists(filepath):
        print("  No daily_thoughts.json found, skipping...")
        return 0
    
    print("Importing daily thoughts...")
    with open(filepath, 'r') as f:
        thoughts_data = json.load(f)
    
    count = 0
    for thought_dict in thoughts_data:
        DailyThought.objects.update_or_create(
            id=thought_dict['id'],
            defaults={
                'content': thought_dict['content'],
                'author': thought_dict.get('author', ''),
                'category': thought_dict.get('category', 'inspiration'),
                'is_active': thought_dict.get('is_active', True),
            }
        )
        count += 1
    
    print(f"  Imported {count} daily thoughts")
    return count

def reset_sequences():
    """Reset PostgreSQL sequences to max ID values"""
    from django.db import connection
    
    print("Resetting PostgreSQL sequences...")
    
    # Tables and their sequence names
    tables = [
        ('auth_user', 'auth_user_id_seq'),
        ('core_userprofile', 'core_userprofile_id_seq'),
        ('core_dailythought', 'core_dailythought_id_seq'),
        ('notes_notefolder', 'notes_notefolder_id_seq'),
        ('notes_note', 'notes_note_id_seq'),
        ('diary_diaryentry', 'diary_diaryentry_id_seq'),
        ('goals_goal', 'goals_goal_id_seq'),
        ('goals_task', 'goals_task_id_seq'),
        ('ai_chat_aiconversation', 'ai_chat_aiconversation_id_seq'),
        ('ai_chat_aimessage', 'ai_chat_aimessage_id_seq'),
    ]
    
    with connection.cursor() as cursor:
        for table, seq in tables:
            try:
                cursor.execute(f"SELECT setval('{seq}', COALESCE((SELECT MAX(id) FROM {table}), 1))")
            except Exception as e:
                print(f"  Warning: Could not reset {seq}: {e}")
    
    print("  Sequences reset complete")

@transaction.atomic
def main():
    print("=" * 50)
    print("JAYTI PostgreSQL Data Import")
    print("=" * 50)
    print(f"Import directory: {EXPORT_DIR}")
    print()
    
    if not os.path.exists(EXPORT_DIR):
        print(f"ERROR: Export directory not found: {EXPORT_DIR}")
        print("Please run export_sqlite_data.py first!")
        sys.exit(1)
    
    total = 0
    total += import_users()
    total += import_note_folders()
    total += import_notes()
    total += import_diary_entries()
    total += import_goals()
    total += import_tasks()
    total += import_chat_sessions()
    total += import_chat_messages()
    total += import_daily_thoughts()
    
    # Reset sequences for PostgreSQL
    reset_sequences()
    
    print()
    print("=" * 50)
    print(f"Import complete! Total records: {total}")
    print("=" * 50)

if __name__ == '__main__':
    main()
