from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
import logging
import json
from .models import User,Post,Like,Follower

from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

logging.basicConfig(level=logging.DEBUG)
def index(request):
    
    posts=Post.objects.filter(poster__in=User.objects.all())
    post_counts=len(posts)
   
    posts=posts.order_by('-timestamp')    
    like_counts=[{post.id:post.post_likes.count()} for post in posts]
   
    key_to_display = 'id'

    for item in like_counts:
        if key_to_display in item:
           
            logging.debug(f'{item[key_to_display]}')
    
    paginator = Paginator(posts, 10) 
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html",{'posts':posts,'like_counts':like_counts,'post_counts':post_counts})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def save_post(request):
    if request.method=="POST":        
        if request.user.is_authenticated:          
            content=request.POST.get('content')
            if content:
                post=Post(poster=request.user,content=content)
                post.save()
                logging.debug(f'post object saved: {post.content}')
                return HttpResponseRedirect(reverse("index"))
        else:
            return redirect('login') 
    return render(request,"network/index.html")

def profile(request,poster_id):
    if request.user.is_authenticated:
        this_user=User.objects.get(pk=poster_id)
        all_user_posts=this_user.posts.all()
        all_user_posts=all_user_posts.order_by('-timestamp')

        post_counts=len(all_user_posts)
        number_of_my_followers=this_user.followers.count()
       
        number_of_my_following=this_user.following_users.count()
        # pagination
        paginator = Paginator(all_user_posts, 4) 
        page = request.GET.get('page', 1)
        try:
            all_user_posts = paginator.page(page)
        except PageNotAnInteger:
            all_user_posts = paginator.page(1)
        except EmptyPage:
            all_user_posts = paginator.page(paginator.num_pages)
            
        # end pagination
       
        return render(request,'network/profile.html',{'posts':all_user_posts,'num_followers':number_of_my_followers,'num_following':number_of_my_following,'poster':this_user,'post_counts':post_counts})
    
    else:
        return redirect('login')  
 
  
def toggle_like(request, post_id):   
    if request.method == "POST":
        post=get_object_or_404(Post,pk=post_id)
        user=request.user
                
        all_likes_this_post=Like.objects.filter(post__id=post_id)
        all_users_liked_this_post=[object.user for object in all_likes_this_post]
        
        if user in all_users_liked_this_post:
            Like.objects.filter(user=user).delete()
            liked=False
        else:
            like=Like.objects.create(user=user,post=post)
            like.save()
            liked=True
            
        posts=Post.objects.all()
        like_counts={post.id:post.post_likes.count() for post in posts}         
        
        return JsonResponse({'liked':liked,'like_counts':like_counts})
    
    else:        
        return JsonResponse({'error found::': 'User not authenticated or method not allowed'}, status=401)
    
def save_follower(request,poster_username):
    if request.user.is_authenticated:
        if request.method=="POST":            
            poster=get_object_or_404(User,username=poster_username)        
            is_already_following=request.user.following_users.filter(followed=poster).exists()            
            if not is_already_following: 
                follower=Follower(follower=request.user,followed=poster)
                follower.save()
            else:
                follower=request.user.following_users.filter(followed=poster) 
                follower.delete() 
            is_following=request.user.following_users.filter(followed=poster).exists()
            logging.debug(f'is_following::{is_following}')
            return HttpResponseRedirect(reverse('profile',args=[poster.id]) + f'?is_following={is_following}')           
    else:
        return redirect('login')
    
def following(request):
    if request.user.is_authenticated:
    
        all_users_i_follow = User.objects.filter(followers__follower=request.user)
        all_users_posts=[]
        
        all_users_posts=Post.objects.filter(poster__in=all_users_i_follow)
        post_counts=len(all_users_posts)
        all_users_posts=all_users_posts.order_by('-timestamp')
        logging.debug(f'all_users_posts::{all_users_posts}')        
        
        paginator = Paginator(all_users_posts, 10) 
        page = request.GET.get('page', 1)
        try:
            all_users_posts = paginator.page(page)
        except PageNotAnInteger:
            all_users_posts = paginator.page(1)
        except EmptyPage:
            all_users_posts = paginator.page(paginator.num_pages)            
       
    return render(request,'network/following.html',{'posts':all_users_posts,'post_counts':post_counts})

def save_content(request,post_id):
    if request.method=="POST":
        content=request.POST.get('content')
        post=get_object_or_404(Post,pk=post_id)
        if content:
            post.content=content
            post.save()
            
    return HttpResponseRedirect(reverse('index'))
        
        
    
    
    
    
        