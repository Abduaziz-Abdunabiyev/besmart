from django.db import models
from django.contrib.auth.models import User

def avatar_upload_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
