from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"{self.user} - {self.content[:20]}"

    def total_likes(self):
        return self.likes.count()
    
class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following = models.ManyToManyField("User", blank=True, related_name="followers")

    def __str__(self):
        return f"{self.user} follows {self.following.count()} users"

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liker")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.user} likes the post {self.post}"