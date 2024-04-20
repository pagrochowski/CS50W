from django.contrib import admin
from .models import *


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'seller', 'active', 'current_bid', 'created_at')
    list_filter = ('active', 'category')
    search_fields = ('title', 'description', 'seller__username')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'bidder', 'listing', 'amount', 'timestamp')
    list_filter = ('listing',)
    search_fields = ('bidder__username',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'commenter', 'listing', 'content', 'timestamp')
    list_filter = ('listing', 'commenter') 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',) 


# Register your models here.
admin.site.register(AuctionListing, AuctionListingAdmin) 
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
