
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
    path("following", views.following_posts, name="following_posts"),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('total-likes/<int:post_id>/', views.post_likes, name='total_likes'),
]