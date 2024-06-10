from django.shortcuts import redirect


def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect("articles:list-template")
        else:
            return redirect("accounts:login")