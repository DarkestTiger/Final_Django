from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("password")
        ret.pop("last_login")
        ret.pop("is_superuser")
        ret.pop("is_staff")
        ret.pop("is_active")
        ret.pop("introduce")
        ret.pop("groups")
        ret.pop("user_permissions")
        return ret

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            #provide django, password will be hashing!
            instance.set_password(password)
        instance.save()
        return instance
    


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {'read_only':True},
            'password': {'write_only':True}
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("last_login")
        ret.pop("is_superuser")
        ret.pop("is_staff")
        ret.pop("is_active")
        ret.pop("groups")
        ret.pop("user_permissions")
        return ret

    
    def validate_password(self, value: str) -> str:
        return make_password(value)