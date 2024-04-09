from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("terlik", views.terlik, name="terlik"),
    path("mati", views.mati, name="mati"),
    path("<str:name>", views.greet, name="greet")
]