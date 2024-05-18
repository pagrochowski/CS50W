
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import json

from .forms import *
from .models import *

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})


@login_required
@require_POST
def edit_post(request, post_id, username=None):
    try:
        post = get_object_or_404(Post, pk=post_id)

        # Authorization check:
        if username is not None:  # Edit from profile page
            if post.user.username != username:
                return JsonResponse({'error': 'You are not authorized to edit this post.'}, status=403)
        else:  # Edit from index page
            if post.user != request.user:
                return JsonResponse({'error': 'You are not authorized to edit this post.'}, status=403)

        # Data handling:
        data = json.loads(request.body)
        new_content = data.get('content')

        if not new_content:
            return JsonResponse({'error': 'Invalid data. Content is required.'}, status=400)

        post.content = new_content
        post.save()

        return JsonResponse({'message': 'Post updated successfully'})

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data")
    
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found.'}, status=404)  

    except Exception as e:  # Catch any other unexpected errors
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500) 


@login_required
def following(request):
    followed_users = Following.objects.filter(user=request.user).values_list('followed_user', flat=True)
    posts_list = Post.objects.filter(user__in=followed_users).order_by('-timestamp')

    paginator = Paginator(posts_list, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')  # Get page number from query parameters
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/following.html', {'page_obj': page_obj})


@login_required
def follow(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    _, created = Following.objects.get_or_create(user=request.user, followed_user=user_to_follow)
    if created:
        return JsonResponse({'message': 'Followed'})
    else:
        Following.objects.filter(user=request.user, followed_user=user_to_follow).delete()
        return JsonResponse({'message': 'Unfollowed'})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    following_count = user.following.all().count()
    follower_count = user.followers.all().count()

    # Check if current user is already following the profile user
    is_following = False
    if request.user.is_authenticated:
        is_following = Following.objects.filter(user=request.user, followed_user=user).exists()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/profile.html', {
        'profile_user': user,
        'posts': posts,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,  # Pass this to the template
        'page_obj': page_obj
    })


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')  # Redirect to the main page or wherever you display posts
    else:
        form = PostForm()
    return render(request, 'network/new_post.html', {'form': form})


def index(request):
    posts_list = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/index.html', {'page_obj': page_obj})


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
