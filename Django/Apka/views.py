from django.shortcuts import render
from django.http import HttpResponse

import testowy

# Create your views here.
def index(request):
    return render(request, "Apka/index.html")

def terlik(request):
    return HttpResponse("Hello, Terlik!")

def mati(request):
    return HttpResponse("Hello, Mati!")

def greet(request, name):
    return render(request, "Apka/greet.html", {
        "name": name.capitalize()
    })