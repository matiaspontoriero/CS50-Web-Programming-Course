from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    return render(request, "network/profile.html", {
        "user": user, 
        "posts": posts
    })

def all_posts(request):
    posts = Post.objects.all()
    return render(request, "network/posts.html", {
        "posts": posts
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

def edit_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        post.content = request.POST["content"]
        post.save()
        return HttpResponseRedirect(reverse("all_posts"))
    else:
        return render(request, "network/edit.html", {
            "post": post
        })