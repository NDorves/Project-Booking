from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def first_view(request):
    return HttpResponse("<h1>Hello! It's my first  Project view!</h1>")
