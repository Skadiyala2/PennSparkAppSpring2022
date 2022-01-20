from rest_framework import serializers
from app.models import Tweet, HashTag, User_Profile
from django.contrib.auth.models import User

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['user', 'content', 'createDate']


class HashTagSerializer(serializers.ModelSerializer):
    #Fields 
    id = serializers.ReadOnlyField()
    class Meta:
        model = HashTag
        fields = ['name', 'id']


class User_ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = User_Profile
        fields = ['avatar', 'bio', 'user', 'followingUsers', 'followingTweets', 'id']
        

class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'id']
