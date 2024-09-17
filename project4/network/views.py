from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import User, Post, Follow, Like


def index(request):
    return render(request, "network/index.html")


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
        Follow.objects.create(user=user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    is_following = Follow.objects.filter(user=request.user, following=user).exists()
    followers = Follow.objects.filter(following=user).count()
    if followers == None:
        followers = 0
    following = Follow.objects.filter(user=user)
    following = following[0].following.count()
    return render(request, "network/profile.html", {
        "user": user, 
        "posts": posts,
        "is_following": is_following,
        "followers": followers,
        "following": following,
    })

def all_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    liked_posts = Like.objects.filter(user=request.user).values_list('post', flat=True)
    return render(request, "network/posts.html", {
        "posts": page_obj,
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })


def create_post(request):
    if request.method == "POST":
        user = request.user
        content = request.POST["content"]
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("all_posts"))
    else:
        return render(request, "network/create.html")
    
def following_posts(request):
    user = request.user
    following_users = Follow.objects.filter(user=user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    return render(request, "network/following.html", {
        "posts": posts
    })

def edit_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.content = request.POST["content"]
        post.save()
        return HttpResponseRedirect(reverse("all_posts"))
    else:
        return HttpResponseForbidden()

@login_required
def follow_user(request, username):
    if request.method == "POST":
        target_user = get_object_or_404(User, username=username)
        if request.user == target_user:
            return JsonResponse({'success': False, 'error': 'You cannot follow yourself'}, status=400)
        follow_instance, created = Follow.objects.get_or_create(user=request.user)
        follow_instance.following.add(target_user)
        followers_count = Follow.objects.filter(following=target_user).count()
        following_count = Follow.objects.filter(user=target_user).count()
        return JsonResponse({
            'success': True,
            'followers_count': followers_count,
            'following_count': following_count,
            'following': True
        })
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def unfollow_user(request, username):
    if request.method == "POST":
        target_user = get_object_or_404(User, username=username)
        if request.user == target_user:
            return JsonResponse({'success': False, 'error': 'You cannot unfollow yourself'}, status=400)
        follow_instance = Follow.objects.get(user=request.user)
        follow_instance.following.remove(target_user)
        followers_count = Follow.objects.filter(following=target_user).count()
        following_count = Follow.objects.filter(user=target_user).count()
        return JsonResponse({
            'success': True,
            'followers_count': followers_count,
            'following_count': following_count,
            'following': False
        })
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@require_POST
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, post=post)
    total_likes = post.total_likes()
    if not created:
        like.delete()
        return JsonResponse({
            'success': True, 
            'liked': False,
            'total_likes': total_likes
        })
    else:
        return JsonResponse({
            'success': True, 
            'liked': True,
            'total_likes': total_likes
        })
    
def post_likes(post_id):
    post = Post.objects.get(id=post_id)
    total_likes = Like.objects.filter(post=post).count()
    return JsonResponse({
        'total_likes': total_likes
    })