from rest_framework import serializers
from .models import Article, Comment, Hashtag
from accounts.serializers import UserSerializer

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('article',)

class ArticleSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True)
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ('hashtags',)
        # image도 마찬가지, views.py에서 처리

class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)