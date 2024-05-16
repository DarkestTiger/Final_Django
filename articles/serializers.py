from rest_framework import serializers
from .models import Article, Comment, Hashtag
from accounts.serializers import UserSerializer

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('article','author','like_users',)
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("article")
        ret.pop("like_users")
        return ret
    def get_like_count(self, instance):
        return instance.like_users.count()

class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    hashtags = HashtagSerializer(many=True)
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ('hashtags','like_users',)
        # image도 마찬가지, views.py에서 처리
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("like_users")
        return ret
    def get_like_count(self, instance):
        return instance.like_users.count()

class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)