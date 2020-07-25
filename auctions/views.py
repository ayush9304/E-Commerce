from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Listing, UserBid, UserComment, User

from datetime import datetime


def index(request):
    listings = Listing.objects.filter(status="active").all()
    return render(request, "auctions/index.html", {
        "listings":reversed(listings)
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.POST.get('image')
        category = request.POST.get('category')
        if not category:
            category = "Category not provided"
        s_bid = request.POST.get('s_bid')
        condition = request.POST.get('condition')
        c_time = datetime.now()
        try:
            listing_ = Listing.objects.create(title=title, description=description, image=image, category=category, starting_bid=s_bid, current_bid=s_bid, condition=condition, create_time=c_time)
            user = User.objects.get(username=request.user.username)
            user.listing.add(listing_)
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            return HttpResponse(f"There was a error while creating the listing. : {e}")
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "auctions/create.html")

def search(request):
    query = request.GET['query']
    listings = Listing.objects.all()
    results = []
    for each in listings:
        title = each.title.lower()
        if title.find(query.lower()) >= 0:
            results.append(each)
    return render(request, "auctions/index.html", {
        "query":query,
        "result_title":f"Search result for '{query}'",
        "listings":reversed(results)
    })

def listing(request, id):
    list_item = Listing.objects.get(id=id)
    watchlist = ""
    watchers_count = Listing.objects.get(id=id).watchers.count()
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.filter(id=id).first
    return render(request, "auctions/listing.html", {
        "list":list_item,
        "creater":list_item.creater.get(),
        "watchlist":watchlist,
        "watchers_count":watchers_count
    })

def watchlist(request):
    if request.user.is_authenticated:
        listings = request.user.watchlist.all()
        return render(request, "auctions/index.html", {
            "result_title":"Watchlist",
            "listings":reversed(listings),
        })
    return HttpResponseRedirect(reverse("login"))

def add_watchlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            id = request.POST['id']
            origin = request.POST['origin']
            list_item = Listing.objects.get(id=id)
            try:
                request.user.watchlist.add(list_item)
            except Exception as e:
                return render(request, "auctions/message.html", {
                    "message":f"There was an error while adding to watchlist : {e}"
                })
            #return HttpResponseRedirect(reverse("listing", args=[id]))
            return HttpResponseRedirect(origin)
        else:
            return HttpResponseRedirect(reverse("login"))

def remove_watchlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            id = request.POST['id']
            origin = request.POST['origin']
            list_item = Listing.objects.get(id=id)
            try:
                watchlist = request.user.watchlist.get(id__contains=id)
                request.user.watchlist.remove(watchlist)
            except Exception as e:
                return render(request, "auctions/message.html", {
                    "message":f"There was an error while removing from watchlist : {e}"
                })
            #return HttpResponseRedirect(reverse("watchlist"))
            return HttpResponseRedirect(origin)
        else:
            return HttpResponseRedirect(reverse("login"))

def my_listing(request):
    if request.user.is_authenticated:
        listings = request.user.listing.all()
        return render(request, "auctions/index.html", {
            "listings":reversed(listings),
            "result_title":"My Listings",
            "creater":True
        })
    else:
        return HttpResponseRedirect(reverse("login"))