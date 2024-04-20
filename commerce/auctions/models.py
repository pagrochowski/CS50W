from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings
from PIL import Image
import os.path


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
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    image = models.ImageField(upload_to='auctions/media', null=True, blank=True, default='auctions/static/auctions/No-Image-Placeholder.png')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_sold")
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="listings_bought")

    def save(self, *args, **kwargs):
        if not self.current_bid:  
            self.current_bid = self.starting_bid

        if self.image:
            super().save(*args, **kwargs)  

            img_path = os.path.join('auctions/media', self.image.path)  
            print(self.image.path)
            img = Image.open(img_path) 

            max_size = (200, 200)  
            print("Image Size Before:", img.size)  
            img.thumbnail(max_size)
            print("Image Size After:", img.size)   
            img.save(img_path)
            print(img_path)

        super().save(*args, **kwargs)  

    
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