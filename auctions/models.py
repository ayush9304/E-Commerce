from django.contrib.auth.models import AbstractUser
from django.db import models

#Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=130)
    image = models.CharField(max_length=1000)
    starting_bid = models.FloatField()
    current_bid = models.FloatField()
    bid_increment = models.FloatField()
    condition = models.CharField(max_length=5)

    def __str__(self):
        return f"(ID: {self.id}) {self.title}"
    

class UserBid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    max_bid = models.FloatField()

class UserComment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}"
    

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchers")
    listing = models.ManyToManyField(Listing, blank=True, related_name="creater")
    bids = models.ManyToManyField(UserBid, blank=True, related_name="bidder")
    comments = models.ManyToManyField(UserComment, blank=True, related_name="commenter")