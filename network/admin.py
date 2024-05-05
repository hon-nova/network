from django.contrib import admin

# Register your models here.

from .models import User,Post,Like,Follower,Like

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Like)
