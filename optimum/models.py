__author__ = 'evangelie'
from django.db import models
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth

class UserCredentials(models.Model):
    id = models.AutoField(primary_key=True)
    #username = models.TextField(db_column='userName', blank=False)  # Field name made lowercase.
    user = models.ForeignKey(User,blank=False)
    #code = models.TextField(db_column='code')  # Field name made lowercase.
    credentials = models.TextField(db_column='credentials', blank=False)  # Field name made lowercase.

class UserFacebookData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserSocialAuth,blank=False)
    likes = models.TextField(db_column='likes', blank=False)  # Field name made lowercase.
    photos = models.TextField(db_column='photos', blank=False)  # Field name made lowercase.
    posts =  models.TextField(db_column='posts', blank=False)

class Rating(models.Model):
    rate = models.CharField(max_length=100)