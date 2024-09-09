from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    followers = models.ManyToManyField("User", blank=True, related_name="user_followers")
    followings = models.ManyToManyField("User", blank=True, related_name="following")

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="liked_posts")

    def __str__(self):
        return f"{self.user}: {self.content[:50]}... At time: {self.timestamp.strftime('%b %d %Y, %I:%M %p')}"