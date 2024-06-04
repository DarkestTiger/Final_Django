from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def article_list_template_view(request):
    return render(request, "articles/article_list.html")


# @login_required
def article_create_template_view(request):
    return render(request, "articles/article_create3.html")


def article_detail_template_view(request, articleId):
    context = {
        "articleId": articleId
    }
    return render(request, "articles/article_detail.html", context)
