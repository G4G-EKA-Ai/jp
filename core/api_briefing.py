from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, timedelta
import google.generativeai as genai

@login_required
def daily_briefing(request):
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Get recent data
        from notes.models import Note
        from diary.models import DiaryEntry
        from goals.models import Goal, Task
        
        recent_notes = Note.objects.filter(user=request.user, created_at__gte=datetime.now()-timedelta(days=7)).count()
        recent_diary = DiaryEntry.objects.filter(user=request.user, entry_date__gte=datetime.now().date()-timedelta(days=7)).count()
        active_goals = Goal.objects.filter(user=request.user, status='active').count()
        pending_tasks = Task.objects.filter(goal__user=request.user, status='pending').count()
        
        # Get latest mood
        latest_entry = DiaryEntry.objects.filter(user=request.user, mood__isnull=False).order_by('-entry_date').first()
        mood_text = dict(DiaryEntry.MOOD_CHOICES).get(latest_entry.mood, "neutral") if latest_entry else "unknown"
        
        prompt = f"""You are Jayti's personal AI companion. Create a warm, personalized morning briefing.

Context:
- Recent activity: {recent_notes} notes, {recent_diary} diary entries this week
- Active goals: {active_goals}
- Pending tasks: {pending_tasks}
- Recent mood: {mood_text}

Create a brief (3-4 sentences) morning message that:
1. Greets warmly
2. Acknowledges recent activity
3. Provides gentle encouragement
4. Suggests one small action for today

Keep it personal, supportive, and concise. No emojis."""

        response = model.generate_content(prompt)
        
        return JsonResponse({
            'success': True,
            'briefing': response.text,
            'stats': {
                'notes': recent_notes,
                'diary': recent_diary,
                'goals': active_goals,
                'tasks': pending_tasks
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'briefing': f"Good morning! You have {active_goals} active goals and {pending_tasks} tasks to work on today.",
            'error': str(e)
        })

@login_required
def weekly_summary(request):
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        from diary.models import DiaryEntry
        from goals.models import Task
        
        week_start = datetime.now().date() - timedelta(days=7)
        
        # Get week's diary entries
        entries = DiaryEntry.objects.filter(user=request.user, entry_date__gte=week_start).order_by('entry_date')
        moods = [e.mood for e in entries if e.mood]
        avg_mood = sum(moods) / len(moods) if moods else 3
        
        # Get completed tasks
        completed = Task.objects.filter(goal__user=request.user, status='completed', completed_at__gte=week_start).count()
        
        prompt = f"""Create a reflective weekly summary for Jayti.

This week:
- Diary entries: {entries.count()}
- Average mood: {avg_mood:.1f}/5
- Tasks completed: {completed}

Create a thoughtful 4-5 sentence summary that:
1. Reflects on the week's emotional journey
2. Celebrates accomplishments
3. Identifies patterns or themes
4. Offers gentle guidance for next week

Be warm, insightful, and supportive. No emojis."""

        response = model.generate_content(prompt)
        
        return JsonResponse({
            'success': True,
            'summary': response.text,
            'stats': {
                'entries': entries.count(),
                'avg_mood': round(avg_mood, 1),
                'completed': completed
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'summary': f"This week you wrote {entries.count()} diary entries and completed {completed} tasks. Keep going!",
            'error': str(e)
        })
