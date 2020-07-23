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
    path("listing/<int:id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("listing/<int:id>/remove_watchlist", views.remove_watchlist, name="remove_watchlist")
]
