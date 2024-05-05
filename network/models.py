from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)    
    
class Follower(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following",)
    followers=models.ForeignKey(User,on_delete=models.CASCADE,related_name="being_followers")
    is_followed=models.BooleanField(default=False)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    

    class Meta:
        unique_together = ['user', 'post']