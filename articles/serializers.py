from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"