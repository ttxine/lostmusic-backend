from django.contrib.auth import get_user_model

from rest_framework import serializers

from src.oauth.models import Follower

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'email', 'display_name', 'about', 'avatar', 'is_staff', 'is_active'


class CustomUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'display_name', 'about', 'avatar', 'is_active'


class FollowingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField('email', read_only=True)
    
    class Meta:
        model = Follower
        fields = 'user',


class FollowerSerializer(serializers.ModelSerializer):
    subscriber = serializers.SlugRelatedField('email', read_only=True)
    
    class Meta:
        model = Follower
        fields = 'subscriber',
