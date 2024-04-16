from django import forms
from .models import AuctionListing


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        labels = { 
            'starting_bid': 'Starting Price'
        }

