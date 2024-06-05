from rest_framework import serializers

from .models import Article, Comment, Hashtag, Saved

from accounts.serializers import UserSerializer
from accounts.models import User

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('article','author','like_users',)
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret
    def get_like_count(self, instance):
        return instance.like_users.count()

class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    hashtags = HashtagSerializer(many=True)
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ('hashtags','like_users','saved_list')
        # image도 마찬가지, views.py에서 처리
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("saved_list")
        return ret
    def get_like_count(self, instance):
        return instance.like_users.count()
    def get_comments_count(self, instance):
        return instance.comments.count()

class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)

class ArticleSavedSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    saved_articles = ArticleSerializer(many=True, read_only=True)
    saved_articles_count = serializers.SerializerMethodField()
    class Meta:
        model = Saved
        fields = "__all__"
    def get_saved_articles_count(self, instance):
        return instance.saved_articles.count()

class UserProfileSerializer(serializers.ModelSerializer):
    posts = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'profile_image', 'posts']