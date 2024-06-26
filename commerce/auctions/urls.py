from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views
from .views import CreateListingView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path('listings/create/', CreateListingView.as_view(), name='create_listing'),
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listings/<int:listing_id>/place_bid', views.place_bid, name='place_bid'),
    path('listings/<int:listing_id>/close_auction', views.close_auction, name='close_auction'),
    path('listings/<int:listing_id>/toggle_watchlist', views.toggle_watchlist, name='toggle_watchlist'),
    path('listings/<int:listing_id>/add_comment', views.add_comment, name='add_comment'),
    path("categories", views.categories_list, name="categories"),
    path("categories/<str:category_name>", views.category_detail, name="category_detail"),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)