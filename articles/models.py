from django.db import models
from accounts.models import User
from django.conf import settings

# Create your models here.
class Hashtag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
class Article(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    # image (로컬/url)
    # image = ...
    # image_url = ...

    # author id
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    # likes
    # like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "like_articles")

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # author id
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    # article id
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    # likes
    # like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_comments")
