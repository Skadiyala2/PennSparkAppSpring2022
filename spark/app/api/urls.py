from django.urls import path
from .views import UserList, ViewUser, UserTweets, HashTagTweets, ViewUserPFP, ManageTweets, FollowHashtags, FollowUser, UserFeed

urlpatterns = [
    #path('', views.apiOverview, name = "api-overview")
    path('', UserList.as_view(), name='user-list'),
    path('users/<str:pk>/', ViewUser.as_view(), name='user-obj'),
    path('manage/tweets/', ManageTweets.as_view(), name='tweet-manager'),
    path('tweets/<str:pk>/', UserTweets.as_view(), name='user-tweets'),
    path('users/pfp/<str:pk>/', ViewUserPFP.as_view(), name='user-pfp'),
    path('hashtweets/<str:pk>/', HashTagTweets.as_view(), name='hashtag-tweets'),
    path('hashfollow/<str:pk>/', FollowHashtags.as_view(), name='hashtag-follow'),
    path('userfollow/<str:pk>/', FollowUser.as_view(), name= 'user-follow'),
    path('userfeed', UserFeed.as_view(), name= 'user-feed'),
]