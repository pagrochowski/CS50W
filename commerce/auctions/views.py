from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import *
from .forms import *


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save yet
            post.user = request.user        # Set the user
            post.save()                     # Now save
            return redirect('index')        # Redirect after saving
    else:
        form = PostForm()

    return render(request, 'network/new_post.html', {'form': form}) 


def categories_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'auctions/categories_list.html', context)

def category_detail(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
        listings = category.listings.filter(active=True) 
        context = {'category': category, 'listings': listings}
        return render(request, 'auctions/category_detail.html', context)
    except Category.DoesNotExist:
        return render(request, "auctions/error.html", {"message": "Category not found."}, status=404) 


@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    watchlist_count = watchlist_items.count()  
    context = {'watchlist_items': watchlist_items, 'watchlist_count': watchlist_count}
    return render(request, 'auctions/watchlist.html', context)


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    user = request.user

    if request.method == "POST":
        content = request.POST['content']
        if content:  
            Comment.objects.create(
                content=content, 
                commenter=user, 
                listing=listing
            )
            messages.success(request, "Your comment has been added!")
        else:
            messages.error(request, "Cannot add an empty comment.") 

    return redirect('listing_detail', listing_id=listing_id)

class CreateListingView(CreateView):
    model = AuctionListing
    form_class = CreateListingForm
    template_name = 'auctions/create_listing.html'

    def form_valid(self, form):
        form.instance.seller = self.request.user 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listing_detail', args=[self.object.id])
    

def listing_detail(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)  
    is_watched = Watchlist.objects.filter(user=request.user, listing=listing).exists() 
    form = CommentForm()

    context = {
        'listing': listing, 
        'is_watched': is_watched,
        'comments': listing.comments.order_by('-timestamp'),
        'comment_form': form
    }

    return render(request, 'auctions/listing_detail.html', context)

@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    user = request.user

    if request.method == "POST":
        new_bid_amount = float(request.POST['bid_amount'])

        if not listing.active:  
            messages.error(request, "Cannot place bids on a closed listing.")
            return redirect('listing_detail', listing_id=listing_id)

        if new_bid_amount <= listing.starting_bid:  
            messages.error(request, "Bid must be greater than the starting bid.")
        elif listing.current_bid and new_bid_amount <= listing.current_bid:  
            messages.error(request, "Bid must be greater than the current highest bid.")
        else:  # Bid is valid
            Bid.objects.create(amount=new_bid_amount, bidder=user, listing=listing)
            listing.current_bid = new_bid_amount  
            listing.save()  
            messages.success(request, "Your bid has been placed!")

        return redirect('listing_detail', listing_id=listing_id)

    else: 
        return redirect('listing_detail', listing_id=listing_id)


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    user = request.user

    if request.method == "POST":
        action = request.POST['action']

        if action == 'add':
            Watchlist.objects.create(user=user, listing=listing)

        elif action == 'remove':
            Watchlist.objects.filter(user=user, listing=listing).delete()

        return redirect('listing_detail', listing_id=listing_id)

    else: 
        return redirect('listing_detail', listing_id=listing_id)


def close_auction(request, listing_id):
    if request.user.is_authenticated:
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        if request.user == listing.seller:
            listing.active = False 
            listing.winner = listing.bids.order_by('-amount').first().bidder 
            listing.save()
            messages.success(request, "Auction Closed!")
        else:
            messages.error(request, "You cannot close listings you did not create.")
    else:
        messages.error(request, "Login required to close auctions.")

    return redirect('listing_detail', listing_id=listing_id)

def index(request):
    active_listings = AuctionListing.objects.filter(active = True)  
    context = {'listings': active_listings}
    return render(request, "auctions/index.html", context)


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




