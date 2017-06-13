import urllib2

from googleapiclient.discovery import build

__author__ = 'evangelie'
import webbrowser
import httplib2
from optimum.models import UserCredentials
from optimum.utils import creds_to_json, creds_from_json
from apiclient import errors
from apiclient import http
import os
from django.http import HttpResponse
from django.template.context import RequestContext
import requests
from django.shortcuts import render, redirect, render_to_response
from optimum.twitter import get_tweets
from optimum.personality import get_profil
import json
from pprint import pprint
from social.apps.django_app.default.models import UserSocialAuth
import oauth2client
from oauth2client import client
from oauth2client import tools
import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors
from models import UserFacebookData

import datetime
from django.conf import settings
from oauth2client.client import OAuth2Credentials, _extract_id_token
#from oauth2client.django_orm import Storage
from gcm import*
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.context_processors import csrf
import sys, traceback

# Home page
def index(request):
    if request.method == 'GET':
        facebook_login = None        
        try:
          facebook_login = request.user.social_auth.get(provider='facebook')
          try:
            get_facebook_data(request)
          except:
            print "could not get facebook data"
            traceback.print_exc()
        except:
          print "user is not authenticated"      
        context = {'request': request, 'user': request.user, 'facebook_login': facebook_login}
        context.update(csrf(request))        
        return render_to_response('mainPage.html', context)        

def get_facebook_data(request):
    social_user = request.user.social_auth.filter(provider='facebook',).first()


    friends_url = u'https://graph.facebook.com/{0}/' \
          u'friends?fields=id,name,location,picture' \
          u'&access_token={1}'.format(
              social_user.uid,
              social_user.extra_data['access_token'],
          )
    likes_url = u'https://graph.facebook.com/{0}/' \
          u'likes?access_token={1}&limit=1000'.format(
              social_user.uid,
              social_user.extra_data['access_token'],
          )
                
    res = requests.get(likes_url)            
    likes= res.text
    tagged_photos_url= u'https://graph.facebook.com/{0}/' \
          u'photos?fields=source&limit=1000&access_token={1}'.format(
              social_user.uid,
              social_user.extra_data['access_token'],
          )            
    res2 = requests.get(tagged_photos_url)            
    tagged_photos = res2.text

    uploaded_photos_url= u'https://graph.facebook.com/{0}/' \
          u'photos/uploaded?fields=source&limit=1000&access_token={1}'.format(
              social_user.uid,
              social_user.extra_data['access_token'],
          )            
    res3 = requests.get(uploaded_photos_url)            
    uploaded_photos = res3.text

    posts_url= u'https://graph.facebook.com/{0}/' \
          u'feed?limit=10000&access_token={1}'.format(
              social_user.uid,
              social_user.extra_data['access_token'],
          )
    res4 = requests.get(posts_url)            
    posts = res4.text

    user_facebook = UserFacebookData.objects.filter(user=social_user)
    if not user_facebook:
        new_user_data = UserFacebookData.objects.create(user = social_user, likes=likes, tagged_photos=tagged_photos, uploaded_photos=uploaded_photos, posts=posts)
        user_data.likes = likes
        user_data.tagged_photos = tagged_photos
        user_data.uploaded_photos = uploaded_photos
        user_data.posts = posts                
    else:
        user_data = UserFacebookData.objects.get(user=social_user)
    return True

