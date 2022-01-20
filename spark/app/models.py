from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_Profile(models.Model):
    # Fields
    avatar = models.ImageField(null=True, default="ADD DEFAULT LATER", blank=True)
    bio = models.TextField(max_length = 200, null = False, blank = True)
    createDate = models.DateTimeField(auto_now_add = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followingUsers = models.ManyToManyField(User, related_name='followed_users', blank = True)
    followingTweets = models.ManyToManyField("HashTag", related_name='followed_tweets', blank = True)
    
    # Metadata
    class Meta:
        ordering = ['-createDate']

    def __str__(self):
        return self.user.username

class Tweet(models.Model):
    #Fields 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length = 200)
    createDate = models.DateTimeField(auto_now_add = True)
    hashtag= models.ManyToManyField(
        "HashTag", related_name='tweets_under_hashtag', blank=True)

    class Meta:
        ordering = ['-createDate']

class HashTag(models.Model):
    #Fields
    name = models.CharField(max_length = 200, unique = True)

    
