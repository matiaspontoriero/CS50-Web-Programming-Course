from django.urls import path, include

from . import views

entry = "Python"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("modify/<str:title>", views.modify, name="modify"),
    path("save/", views.save, name="save"),
    path("aleatory/", views.aleatory, name="aleatory"),
    ]
