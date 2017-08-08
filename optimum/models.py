__author__ = 'evangelie'
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from social.apps.django_app.default.models import UserSocialAuth

from clarifai import rest
from clarifai.rest import ClarifaiApp
import json, codecs
from credentials import *
from actions import export_as_csv_action

class UserCredentials(models.Model):
    id = models.AutoField(primary_key=True)
    #username = models.TextField(db_column='userName', blank=False)  # Field name made lowercase.
    user = models.ForeignKey(User,blank=False)
    #code = models.TextField(db_column='code')  # Field name made lowercase.
    credentials = models.TextField(db_column='credentials', blank=False)  # Field name made lowercase.

class UserFacebookData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserSocialAuth,blank=False)
    likes = models.TextField(db_column='likes', blank=False, default='')  # Field name made lowercase.
    tagged_photos = models.TextField(db_column='tagged_photos', blank=False, default='')  # Field name made lowercase.
    uploaded_photos = models.TextField(db_column='uploaded_photos', blank=False, default='')  # Field name made lowercase.
    posts =  models.TextField(db_column='posts', blank=False, default='')

class UserFacebookPhotoAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserSocialAuth,blank=False)
    photo = models.TextField(db_column='photo', blank=False)
    keywords =  models.TextField(db_column='keywords', blank=False)

class UserFacebookPostsAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserSocialAuth,blank=False)
    post = models.TextField(db_column='post', blank=False, default='')

class UserFacebookLikesAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserSocialAuth,blank=False)
    like = models.TextField(db_column='like', blank=False, default='')

class AggregatedFacebookDataAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserSocialAuth,blank=False)
    posts_text = models.TextField(db_column='posts_text', blank=False, default='')
    images_text = models.TextField(db_column='images_text', blank=False, default='')
    likes_text = models.TextField(db_column='likes_text', blank=False, default='')

def analyze_facebook_data(modeladmin, request, queryset):
    for entry in queryset:
        tagged_photos_json = json.loads(entry.tagged_photos)
        all_photo_tags = []
        UserFacebookPhotoAnalysis.objects.filter(user=entry.user).delete()
        for photo in tagged_photos_json['data']:
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
                all_photo_tags.append(concept["name"])
            new_UserFacebookPhotoAnalysis = UserFacebookPhotoAnalysis.objects.create(user = entry.user, photo=photo["source"], keywords=keywords)
            new_UserFacebookPhotoAnalysis.save()
        uploaded_photos_json = json.loads(entry.uploaded_photos)
        for photo in uploaded_photos_json['data']:
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
                all_photo_tags.append(concept["name"])
            new_UserFacebookPhotoAnalysis = UserFacebookPhotoAnalysis.objects.create(user = entry.user, photo=photo["source"], keywords=keywords)
            new_UserFacebookPhotoAnalysis.save()

        UserFacebookPostsAnalysis.objects.filter(user=entry.user).delete()
        posts_json = json.loads(entry.posts)
        all_posts = []
        for post in posts_json['data']:
            if 'message' in post.keys():
                print post['message'].encode("utf-8")
                new_UserFacebookPostsAnalysis = UserFacebookPostsAnalysis.objects.create(user = entry.user, post=post['message'].encode("utf-8"))
                all_posts.append(post['message'].encode("utf-8"))
            else:
                print "no message"

        UserFacebookLikesAnalysis.objects.filter(user=entry.user).delete()
        likes_json = json.loads(entry.likes)
        all_likes = []
        for like in likes_json['data']:
            if 'name' in like.keys():
                print like['name'].encode("utf-8")
                new_UserFacebookLikesAnalysis = UserFacebookLikesAnalysis.objects.create(user = entry.user, like=like['name'].encode("utf-8"))
                all_likes.append(like['name'].encode("utf-8"))
            else:
                print "no name"

        AggregatedFacebookDataAnalysis.objects.filter(user=entry.user).delete()
        AggregatedFacebookDataAnalysis.objects.create(user = entry.user, posts_text=','.join(all_posts), likes_text=','.join(all_likes), images_text=','.join(all_photo_tags))

analyze_facebook_data.short_description = "Analyze facebook data"

class UserFacebookDataAdmin(admin.ModelAdmin):
    actions = [analyze_facebook_data]
admin.site.register(UserFacebookData, UserFacebookDataAdmin)

class UserFacebookPhotoAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo','keywords')
    search_fields = ['user__user__username',]
    list_filter = ('user',)
    actions = [export_as_csv_action("CSV Export", fields=['user', 'photo','keywords'])]
    pass
admin.site.register(UserFacebookPhotoAnalysis, UserFacebookPhotoAnalysisAdmin)

class UserFacebookPostsAnalysisAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserFacebookPostsAnalysis, UserFacebookPostsAnalysisAdmin)

class UserFacebookLikesAnalysisAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserFacebookLikesAnalysis, UserFacebookLikesAnalysisAdmin)

class AggregatedFacebookDataAnalysisAdmin(admin.ModelAdmin):
    pass
admin.site.register(AggregatedFacebookDataAnalysis, AggregatedFacebookDataAnalysisAdmin)