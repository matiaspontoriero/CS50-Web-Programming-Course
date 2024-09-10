from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("filter-categories", views.filter_categories, name="filter-categories"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("add-to-watchlist/<int:id>/", views.add_to_watchlist, name="add-to-watchlist"),
    path("remove-watchlist/<int:id>/", views.remove_watchlist, name="remove-watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add-comment/<int:id>", views.add_comment, name="add-comment"),
    path("delete-comment/<int:id>", views.delete_comment, name="delete-comment"),
    path("close-listing/<int:id>", views.close_listing, name="close-listing"),
    path("bid/<int:id>", views.bid, name="bid"),
]
