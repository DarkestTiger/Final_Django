from django.contrib.auth.decorators import login_required
from django.shortcuts import render , get_object_or_404



def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


@login_required
def modify(request):
    user = request.user
    context = {
        "username":user.username,
        "password":user.password,
        "email":user.email,
        "introduce":user.introduce,
        "profile_img":user.profile_img
    }

    return render(request, 'modify.html', context)


def delete(request):
    return render(request, 'delete.html')