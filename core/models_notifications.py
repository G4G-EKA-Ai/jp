"""
Push Notification Models for JAYTI
"""
from django.db import models
from django.contrib.auth.models import User


class PushSubscription(models.Model):
    """Store web push subscription data"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.TextField()
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'endpoint']

    def __str__(self):
        return f"Push Subscription for {self.user.username}"


class NotificationSchedule(models.Model):
    """User notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_schedule')
    briefing_enabled = models.BooleanField(default=True)
    briefing_time = models.TimeField(default='08:00')
    reminder_enabled = models.BooleanField(default=True)
    weekly_summary_enabled = models.BooleanField(default=True)
    weekly_summary_day = models.IntegerField(default=0)  # 0=Monday
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification Schedule for {self.user.username}"
