
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("profile/<str:username>", views.profile, name="profile"), 
    path("all-posts", views.all_posts, name="all_posts"),
    path("create-post", views.create_post, name="create_post"),
    path("edit-post", views.edit_post, name="edit_post"),
]
