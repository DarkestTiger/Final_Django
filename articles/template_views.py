from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Article, Comment, Saved

def article_list_template_view(request):
    return render(request, "articles/article_list.html")


@login_required
def article_create_template_view(request):
    return render(request, "articles/article_create3.html")

@login_required
def article_detail_template_view(request, articleId):
    article = get_object_or_404(Article, pk=articleId)
    like_users = article.like_users.all()
    saved = request.user.saved.all()
    context = {
        "articleId": articleId,
        "article": article,
        "like_users":like_users,
        "saved": saved
    }
    return render(request, "articles/article_detail.html", context)

@login_required
def article_update_template_view(request, articleId):
    article = get_object_or_404(Article, pk=articleId)
    context = {
        "article": article,
        "articleId": articleId
    }
    return render(request, "articles/article_update.html", context)

def comment_detail_view(request, commentId):
    comment = get_object_or_404(Comment, pk=commentId)
    like_users = comment.like_users.all()
    context={
        "comment": comment,
        "commentId": commentId,
        "like_users": like_users
    }
    return render(request, "articles/comment_detail.html", context)

def saved_list_template_view(request):
    return render(request, "articles/saved_list.html")

@login_required
def saved_create_template_view(request):
    return render(request, "articles/saved_create.html")

def saved_detail_template_view(request, savedId):
    saved = get_object_or_404(Saved, pk=savedId)
    context={
        "saved": saved,
        "savedId": savedId
    }
    return render(request, "articles/saved_detail.html", context)

@login_required
def saved_update_template_view(request, savedId):
    saved = get_object_or_404(Saved, pk=savedId)
    context={
        "saved": saved,
        "savedId": savedId
    }
    return render(request, "articles/saved_update.html", context)