from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import AuctionListing, User
from .forms import CreateListingForm
from django.views.generic import CreateView


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
    listing = get_object_or_404(AuctionListing, pk=listing_id)  # Change this later when adding error handling
    context = {'listing': listing}
    return render(request, 'auctions/listing_detail.html', context) 

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




