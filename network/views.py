from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
import logging
import json
from .models import User,Post,Like
from django.utils.html import escapejs

logging.basicConfig(level=logging.DEBUG)
def index(request):
    
    posts=Post.objects.filter(poster__in=User.objects.all())
    posts=posts.order_by('-timestamp')
    return render(request, "network/index.html",{'posts':posts,})

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
        user_followers=this_user.followers.all()
       
        user_following=this_user.following.all()    
        # all posts of this user,reverse order
        user_posts=this_user.posts.all()
        user_posts=user_posts.order_by('-created_at')
        # MUST KNOW user must log in to display Follow or Unfollow btn
        return render(request,'network/profile.html',{'followers':user_followers,'following':user_following, 'all_posts':user_posts})
    
    else:
        return redirect('login')
    
# def toggle_like(request,post_id):
#     if request.user.is_authenticated and request.method=="POST":
#         post=get_object_or_404(Post,pk=post_id)  
#         data=request.body
#         logging.debug(f'data::{data}')
#         logging.debug(f'post_id::{post_id}')
#         try:
#             like,created = Like.objects.get(user=request.user, post=post)
#             like.delete()
#             is_liked = False
#         except Like.DoesNotExist:
#             like = Like(user=request.user, post=post)
#             like.save()
#             is_liked = True 
#         except Exception as e:   
            
#             return JsonResponse({'error found::':str(e)},status=501)  
        
#         likes_count=Like.objects.filter(post=post).count()   
#         return JsonResponse({'likes_count':likes_count,'is_liked':is_liked})
       
#     else:
#         return JsonResponse({'ERROR USER FOUND::': 'User not authenticated'},status=401)

def toggle_like(request, post_id):
    if request.user.is_authenticated and request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        data=request.body
        # logging.debug(f'data::{data}')     
        # logging.debug(f'post_id::{post_id}')
        
        try:
            # Attempt to retrieve the like object for the current user and post
            like = Like.objects.get(user=request.user, post=post)            
            # If the like object exists, delete it (unlike the post)
            like.delete()
            is_liked = False            
        except Like.DoesNotExist:
            # If the like object does not exist, create it (like the post)
            like = Like(user=request.user, post=post)
            like.save()
            is_liked = True

        likes_count = Like.objects.filter(post=post).count()       
        response_data={'likes_count':likes_count,'is_liked':is_liked,}
        
        # Serialize and escape the JSON data
        serialized_data = escapejs(json.dumps(response_data))
        # save/store in session
        request.session['likes_data']=serialized_data
        logging.debug(f'SERIALIZED_DATA ::{serialized_data}')
        logging.debug(f'response_data bare::{response_data}')
        
        return HttpResponseRedirect(reverse('index'))
    else:
        # Return error response if user is not authenticated or request method is not POST
        return JsonResponse({'error found::': 'User not authenticated or method not allowed'}, status=401)
        