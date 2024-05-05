
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('posts',views.save_post,name="posts"),
    path('profile/<int:poster_id>',views.profile,name="profile"),
    path('likes/<int:post_id>',views.toggle_like,name="likes")
]
