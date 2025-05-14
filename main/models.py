
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Content


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')  # Adding related_name to avoid conflicts
#     content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='likes')  # Adding related_name to avoid conflicts
#     timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    timestamp = models.DateTimeField(auto_now_add=True)
    
 
# class Content(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='main_contents')
#     content_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
#     content_file = models.FileField(upload_to='uploads/')
#     description = models.TextField()
#     upload_time = models.DateTimeField(auto_now_add=True)    
