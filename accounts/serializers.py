from rest_framework import serializers

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

    
    def Updates(self, instance, validated_data):
        user = super().update(instance, validated_data)
        username = user.username
        password = user.password
        email = user.email
        profile_img = user.profile_img
        address = user.address
        user.set_username(username)
        user.set_password(password)
        user.set_email(email)
        user.set_profile_img(profile_img)
        user.set_address(address)
        user.save()
        return user