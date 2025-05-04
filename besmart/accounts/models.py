from django.db import models
from django.contrib.auth.models import User

def avatar_upload_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    social_links = models.JSONField(blank=True, null=True)  # Store links like LinkedIn, Twitter
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    achievements = models.JSONField(blank=True, null=True)  # Store user achievements or badges
    notification_preferences = models.JSONField(blank=True, null=True)  # Store preferences for notifications

    def __str__(self):
        return self.user.username
