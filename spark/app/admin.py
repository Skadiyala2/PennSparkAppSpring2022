from django.contrib import admin
from .models import User_Profile, Tweet, HashTag

# Register your models here.
admin.site.register(User_Profile)
admin.site.register(Tweet)
admin.site.register(HashTag)