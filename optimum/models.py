__author__ = 'evangelie'
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from social.apps.django_app.default.models import UserSocialAuth

from clarifai import rest
from clarifai.rest import ClarifaiApp
import json, codecs
from credentials import *

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

class UserFacebookPhotoAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserSocialAuth,blank=False)
    photo = models.TextField(db_column='photo', blank=False)
    keywords =  models.TextField(db_column='keywords', blank=False)

def analyze_facebook_data(modeladmin, request, queryset):
    for entry in queryset:
        photos_json = json.loads(entry.photos)
        for photo in photos_json['data']:
            print photo["source"]
            app = ClarifaiApp(CLARIFAI_APP_ID, CLARIFAI_APP_SECRET)
            # get the general model
            model = app.models.get("general-v1.3")
            # predict with the model
            response = model.predict_by_url(url=photo["source"])            
            #concepts_json = json.loads(response)            
            keywords = ""
            for concept in response['outputs'][0]['data']['concepts']:
                keywords = keywords + " " + concept["name"]
            new_UserFacebookPhotoAnalysis = UserFacebookPhotoAnalysis.objects.create(user = entry.user, photo=photo["source"], keywords=keywords)
            new_UserFacebookPhotoAnalysis.save()

analyze_facebook_data.short_description = "Analyze facebook data"

class UserFacebookDataAdmin(admin.ModelAdmin):
    actions = [analyze_facebook_data]
admin.site.register(UserFacebookData, UserFacebookDataAdmin)

class UserFacebookPhotoAnalysisAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserFacebookPhotoAnalysis, UserFacebookPhotoAnalysisAdmin)