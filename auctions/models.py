from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime
#Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=130)
    description = models.TextField()
    image = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=45, default='No category provided')
    starting_bid = models.FloatField()
    current_bid = models.FloatField()
    condition = models.CharField(max_length=5)
    status = models.CharField(max_length=15, default='active')
    create_time = models.DateTimeField(datetime.now())

    def __str__(self):
        return f"(ID: {self.id}) {self.title}"
    


class UserComment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}"
    

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchers")
    listing = models.ManyToManyField(Listing, blank=True, related_name="creater")
    #bids = models.ManyToManyField(UserBid, blank=True, related_name="bidder")
    comments = models.ManyToManyField(UserComment, blank=True, related_name="commenter")

    def __str__(self):
        return f"{self.username}"
    

class UserBid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    listing = models.ManyToManyField(Listing, related_name="bids")
    bid = models.FloatField()
    time = models.DateTimeField(datetime.now)

    def __str__(self):
        return f"{self.bidder} : [{self.listing.first()}]  US ${self.bid}"