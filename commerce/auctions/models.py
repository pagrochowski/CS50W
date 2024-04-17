from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True) 

    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    active = models.BooleanField(default=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='auctions/media', null=True) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_sold")

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_placed")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watched_listings")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchers")