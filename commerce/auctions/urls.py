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
    path('listings/create/', CreateListingView.as_view(), name='create_listing'),
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)