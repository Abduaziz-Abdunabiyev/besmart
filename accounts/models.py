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

# class Content(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
#     content_file = models.FileField(upload_to='uploads/')
#     upload_time = models.DateTimeField(auto_now_add=True)
#     description = models.TextField(blank=True)
#     likes = models.PositiveIntegerField(default=0)
#     tags = models.CharField(max_length=255, blank=True)
#     duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in seconds for videos")

#     def __str__(self):
#         return f"{self.user.username} - {self.content_type}"

import subprocess

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    content_file = models.FileField(upload_to='uploads/')
    upload_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    likes = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=255, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем файл, чтобы был доступ к пути

        if self.content_type == 'video' and self.content_file:
            try:
                # Путь к файлу
                filepath = self.content_file.path

                # Команда ffprobe (часть ffmpeg) для получения длительности видео в секундах
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
                     '-of', 'default=noprint_wrappers=1:nokey=1', filepath],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
                duration_seconds = float(result.stdout)
                self.duration = int(duration_seconds)

                # Обновляем запись в базе
                Content.objects.filter(pk=self.pk).update(duration=self.duration)

            except Exception as e:
                print(f"Ошибка при получении длительности видео: {e}")


    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'content']),
        ]
