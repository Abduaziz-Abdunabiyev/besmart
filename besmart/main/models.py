
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Content

<<<<<<< HEAD

# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')  # Adding related_name to avoid conflicts
#     content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='likes')  # Adding related_name to avoid conflicts
#     timestamp = models.DateTimeField(auto_now_add=True)
=======
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
>>>>>>> origin/gulmira

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    timestamp = models.DateTimeField(auto_now_add=True)
