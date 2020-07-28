from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime
#Create your models here.

class Category(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class Listing(models.Model):
    title = models.CharField(max_length=130)
    description = models.TextField(max_length=208)
    image = models.CharField(max_length=1000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing")
    starting_bid = models.FloatField()
    current_bid = models.FloatField()
    condition = models.CharField(max_length=5)
    status = models.CharField(max_length=15, default='active')
    create_time = models.DateTimeField(datetime.now())

    def __str__(self):
        return f"(ID: {self.id}) {self.title}"
    

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchers")
    listing = models.ManyToManyField(Listing, blank=True, related_name="creater")
    bought_items = models.ManyToManyField(Listing, blank=True, related_name="buyer")

    def __str__(self):
        return f"{self.username}"
    

class UserBid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    listing = models.ManyToManyField(Listing, related_name="bids")
    bid = models.FloatField()
    time = models.DateTimeField(datetime.now)

    def __str__(self):
        return f"{self.bidder} : [{self.listing.first()}]  US ${self.bid}"


class UserComment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    listing = models.ManyToManyField(Listing, related_name="comments")
    comment = models.TextField()
    time = models.DateTimeField(datetime.now)

    def __str__(self):
        return f"{self.commenter} : [{self.listing.first()}] {self.comment}"