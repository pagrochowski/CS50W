from django import forms
from .models import AuctionListing, Comment


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        labels = { 
            'starting_bid': 'Starting Price'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add your comment here'})
        }
        