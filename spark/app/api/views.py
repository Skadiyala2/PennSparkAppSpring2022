from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from rest_framework import mixins
from django.db.models import Q

from app.models import Tweet, HashTag, User_Profile
from django.contrib.auth.models import User
from app.api.serializers import TweetSerializer, UserSerializer, HashTagSerializer, User_ProfileSerializer 

class UserList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ViewUser(APIView):
    def get_user(self, pk):
        try: 
            return User.objects.get(username=pk)
        except User.DoesNotExist:
            return Http404
    
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        return Response(UserSerializer(user).data)
    
    def post(self, request, pk, format = None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.save()
            model.save()
            user_pfp = User_Profile()
            user_pfp.user = model
            user_pfp.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewUserPFP(APIView):
    def get_user_pfp(self, pk):
        try: 
            return User_Profile.objects.get(user = (User.objects.get(username = pk)))
        except User_Profile.DoesNotExist:
            return Http404
    
    def get(self, request, pk, format=None):
        user_pfp = self.get_user_pfp(pk)
        return Response(User_ProfileSerializer(user_pfp).data)
    
    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            model = User_Profile.objects.get(user = request.user)
            model.bio = request.data['bio']
            model.save()
            return Response(User_ProfileSerializer(model).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserTweets(APIView):
    def get_tweets(self, pk):
        try: 
            user = User.objects.get(username = pk)
            return Tweet.objects.filter(user=user)
        except User.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        tweet = self.get_tweets(pk)
        return Response(TweetSerializer(tweet,many=True).data)
    

class HashTagTweets(APIView):
    def get_tweets(self, pk):
        try: 
            hashtag = HashTag.objects.get(name = pk)
            return hashtag.tweets_under_hashtag.all()
        except User.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        tweet = self.get_tweets(pk)
        return Response(TweetSerializer(tweet,many=True).data)

class ManageTweets (APIView):
    def get_tweets(self, pk):
        try: 
            user = User.objects.get(username = pk)
            return Tweet.objects.filter(user=user)
        except User.DoesNotExist:
            return Http404

    def post(self, request, format=None):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            content = request.data['content']
            tags = {word.strip("#") for word in content.split() if word.startswith("#")}
            model = serializer.save()
            for word in tags:
                try:
                    hashtag = HashTag.objects.get(name = word)
                except HashTag.DoesNotExist:
                    hashtag = HashTag()
                    hashtag.name = word
                    hashtag.save()
                model.hashtag.add(hashtag)
                model.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        if request.user.is_authenticated:
            tweet = self.get_tweets(request.user.username)
            return Response(TweetSerializer(tweet,many=True).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowHashtags(APIView):
    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            try:
                hashtag = HashTag.objects.get(name = pk)
            except:
                hashtag = HashTag()
                hashtag.name = pk
                hashtag.save()
            user = User_Profile.objects.get(user = request.user)
            if user.followingTweets.contains(hashtag):
                user.followingTweets.remove(hashtag)
            else:
                user.followingTweets.add(hashtag)
            user.save()
            return Response(User_ProfileSerializer(user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowUser(APIView):
    def get(self, request, pk, format=None):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(username = pk)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user_host = User_Profile.objects.get(user = request.user)
            if user_host.followingUsers.contains(user):
                user_host.followingUsers.remove(user)
            else:
                user_host.followingUsers.add(user)
            user_host.save()
            return Response(User_ProfileSerializer(user_host).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFeed(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            user_pfp = User_Profile.objects.get(user = request.user)
            tweetList = Tweet.objects.filter(Q(user__in = (user_pfp.followingUsers.all())) |
                                            Q(user = request.user))
            for hashtag in user_pfp.followingTweets.all():
                tweetList = tweetList | hashtag.tweets_under_hashtag.all()
            return Response(TweetSerializer(tweetList, many=True).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)