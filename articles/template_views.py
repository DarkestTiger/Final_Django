from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Article, Comment

def article_list_template_view(request):
    return render(request, "articles/article_list.html")


@login_required
def article_create_template_view(request):
    return render(request, "articles/article_create3.html")


def article_detail_template_view(request, articleId):
    article = get_object_or_404(Article, pk=articleId)
    like_users = article.like_users.all()
    context = {
        "articleId": articleId,
        "article": article,
        "like_users":like_users
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