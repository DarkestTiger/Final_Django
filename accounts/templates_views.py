from django.shortcuts import render


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def profile(request):
    return render(request, 'profile.html')


def modify(request):
    return render(request, 'modify.html')


def delete(request):
    return render(request, 'delete.html')