import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Function to determine the upload path for avatars
def avatar_upload_path(instance, filename):
    # Save avatar images in 'avatars/user_<user_id>/avatar.jpg'
    return os.path.join('avatars', f'user_{instance.user.id}', filename)

# Profile model for extending the User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    contact_preferences = models.TextField(blank=True, null=True)
    content_preferences = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    video_uploads = models.PositiveIntegerField(default=0)
    photo_uploads = models.PositiveIntegerField(default=0)
    subscribers = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


    def __str__(self):
        return self.user.username

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    content_file = models.FileField(upload_to='uploads/')
    upload_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    likes = models.PositiveIntegerField(default=0)  # Новое поле
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'content']),
        ]
