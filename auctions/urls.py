from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("listing/<int:id>/place_bid", views.place_bid, name="place_bid"),
    path("listing/<int:id>/bid/<str:status>", views.listing, name="bid_result")
]
