from django.shortcuts import render


def article_list_template_view(request):
    return render(request, "articles/article_list.html")


def article_create_template_view(request):
    return render(request, "articles/article_create.html")


def article_detail_template_view(request, articleId):
    context = {
        "articleId": articleId
    }
    return render(request, "articles/article_detail.html", context)
