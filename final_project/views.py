from django.shortcuts import render
from django.contrib import redirects

def home(request):
    return render(request,"login.html")