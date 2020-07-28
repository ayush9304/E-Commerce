from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import *

from datetime import datetime


def index(request):
    listings = Listing.objects.filter(status="active")
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
        category_code = request.POST.get('category')
        if not category_code:
            category_code = "CNP"
        category = Category.objects.get(code=category_code)
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

def listing(request, id, status="None"):
    list_item = Listing.objects.get(id=id)
    watchlist = ""
    watchers_count = list_item.watchers.count()
    no_of_bids = UserBid.objects.filter(listing=list_item).count()
    bids = UserBid.objects.filter(listing=list_item).all().order_by('-id')[:5]
    comments = UserComment.objects.filter(listing=list_item).all().order_by('-id')
    creater = list_item.creater.get()
    outbid = ""
    if request.user.is_authenticated:
        if (no_of_bids > 0):
            userBids = UserBid.objects.filter(bidder=request.user, listing=list_item)
            if userBids:
                userBid = max([userBid.bid for userBid in userBids])
                if userBid == list_item.current_bid:
                    outbid = "no"
                else:
                    outbid = "yes"
    if list_item.status == "sold":
        if request.user == list_item.buyer.get():
            success = True
            message = "Congratulations! you have won this auction."
        else:
            success = False
            message = ""
    else:
        success = False
        message = ""
    if request.user == creater:
        creater_view = True
    else:
        creater_view = False
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.filter(id=id).first()
    if status == "success":
        success = True
        message = "Congratulations! You have successfully placed your bid."

    elif status == "error_code1":
        success = False
        message = f"Error: Bid amount must be greater than or equal to US ${list_item.starting_bid}"
    elif status == "error_code2":
        success = False
        message = f"Error: Bid amount must be greater than US ${list_item.current_bid}"
    elif status == "error_code3":
        success = False
        message = "There was an error while placing your bid."
    return render(request, "auctions/listing.html", {
        "list":list_item,
        "creater":creater,
        "watchlist":watchlist,
        "watchers_count":watchers_count,
        "outbid":outbid,
        "no_of_bids":no_of_bids,
        "bids":bids,
        "comments":comments,
        "creater_view":creater_view,
        "success":success,
        "message":message
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

def place_bid(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            bid_amount = float(request.POST['bid'])
            list_id = request.POST.get('id')
            list_item = Listing.objects.get(id=list_id)
            bid_time = datetime.now()
            try:
                if UserBid.objects.filter(listing=list_item).count() == 0:
                    if bid_amount < list_item.starting_bid:
                        return HttpResponseRedirect(reverse("bid_result", kwargs={
                            "id":list_id,
                            "status":"error_code1"
                        }))
                else:
                    if bid_amount <= list_item.current_bid:
                        return HttpResponseRedirect(reverse("bid_result", kwargs={
                            "id":list_id,
                            "status":"error_code2"
                        }))
                list_item.current_bid = bid_amount
                list_item.save()
                user_bid = UserBid.objects.create(bidder=request.user, bid=bid_amount, time=bid_time)
                user_bid.listing.add(list_item)
                user_bid.save()
                return HttpResponseRedirect(reverse("bid_result", kwargs={
                    "id":list_id,
                    "status":"success"
                }))
            except expression as e:
                return HttpResponseRedirect(reverse("bid_result", kwargs={
                    "id":list_id,
                    "status":"error_code3"
                    }))
        else:
            return HttpResponseRedirect(reverse("login"))

def bids(request, id):
    list_item = Listing.objects.get(id=id)
    bids = UserBid.objects.filter(listing=list_item).all().order_by('-id')
    creater = list_item.creater.get()
    if request.user == creater:
        creater_view = True
    else:
        creater_view = False
    return render(request, "auctions/bids.html", {
        "bids":bids,
        "list":list_item,
        "creater_view":creater_view
    })

def auction_command(request):
    if request.method == "POST":
        list_id = int(request.POST['id'])
        list_item = Listing.objects.get(id=list_id)
        if list_item.status == "active":
            if list_item.bids.count() == 0:
                list_item.status = "unsold"
                list_item.save()
            else:
                list_item.status = "sold"
                bids = UserBid.objects.filter(listing=list_item)
                mbid = bids.aggregate(Max('bid'))
                highest_bid = bids.filter(bid=mbid['bid__max']).first()
                highest_bid.bidder.bought_items.add(list_item)
                highest_bid.save()
                list_item.save()
        elif list_item.status == "unsold":
            list_item.status = "active"
            list_item.save()
        return HttpResponseRedirect(reverse("listing", args={list_id}))

def add_comment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            list_id = int(request.POST['id'])
            comment_data = request.POST['comment']
            list_item = Listing.objects.get(id=list_id)
            comment_time = datetime.now()
            user_comment = UserComment.objects.create(commenter=request.user, comment=comment_data, time=comment_time)
            user_comment.listing.add(list_item)
            user_comment.save()
            return HttpResponseRedirect(reverse("listing", args={list_id}))
        else:
            return HttpResponseRedirect(reverse("login"))

def categories(request, category_code=None):
    if category_code == None:
        return render(request, "auctions/categories.html")
    else:
        category = Category.objects.get(code=category_code)
        listings = Listing.objects.filter(category=category, status="active").all()
        return render(request, "auctions/index.html", {
            "listings":listings,
            "result_title":f"Categories > {category.name}"
        })