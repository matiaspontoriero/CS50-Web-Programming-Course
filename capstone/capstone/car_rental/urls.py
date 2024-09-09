from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("renting", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search_cars, name="search"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("car/<str:licence_plate>/", views.load_car, name="car"),
    path("cars/", views.get_cars, name="get_cars"),
    path("book/<str:licence_plate>/", views.book_car, name="book"),
    path("profile/<str:username>/edit", views.edit_profile, name="edit_profile"),
    path("staff", views.staff, name="staff"),
    path('users/', views.get_users, name='get_users'),
    path("profile/<str:username>/delete", views.delete_profile, name="delete_profile"),
]