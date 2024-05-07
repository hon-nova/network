from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass    
    
class Follower(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following_users",)
    followed=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")
    is_followed=models.BooleanField(default=False)
    
    def __str__(self):
        return f'follower_id:{self.id}, the follower::{self.follower.username}'

class Post(models.Model):
    poster=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
        
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")    

    class Meta:
        unique_together = ['user', 'post']
        
    @classmethod    
    def get_posts_num_likes(cls):
        posts_num_likes={}
        
        # step 1: get all posts that are liked
        liked_posts= cls.objects.values('post').annotate(num_likes=models.Count('post'))
        
        for liked_post in liked_posts:
            post_id=liked_post['post']
            num_likes=liked_post['num_likes']
            posts_num_likes[post_id]=num_likes
            
        return posts_num_likes        
       