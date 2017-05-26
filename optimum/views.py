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

# Home page
def index(request):
    if request.method == 'GET':
        
        try:
            social_user = request.user.social_auth.filter(provider='facebook',).first()


            url = u'https://graph.facebook.com/{0}/' \
                  u'friends?fields=id,name,location,picture' \
                  u'&access_token={1}'.format(
                      social_user.uid,
                      social_user.extra_data['access_token'],
                  )
            url = u'https://graph.facebook.com/{0}/' \
                  u'likes?access_token={1}&limit=1000'.format(
                      social_user.uid,
                      social_user.extra_data['access_token'],
                  )
                        
            res = requests.get(url)            
            likes= res.text
            url2= u'https://graph.facebook.com/{0}/' \
                  u'photos?fields=source&limit=1000&access_token={1}'.format(
                      social_user.uid,
                      social_user.extra_data['access_token'],
                  )            
            res2 = requests.get(url2)            
            photos = res2.text
            url3= u'https://graph.facebook.com/{0}/' \
                  u'feed?limit=10000&access_token={1}'.format(
                      social_user.uid,
                      social_user.extra_data['access_token'],
                  )
            res3 = requests.get(url3)            
            posts = res3.text

            user_facebook = UserFacebookData.objects.filter(user=social_user)
            if not user_facebook:
                new_user_data = UserFacebookData.objects.create(user = social_user, likes=likes, photos=photos, posts=posts)
                user_data.likes = likes
                user_data.photos = photos
                user_data.posts = posts                
            else:
                user_data = UserFacebookData.objects.get(user=social_user)
                
        except:
            print('not auth')
        
        try:
            facebook_login = request.user.social_auth.get(provider='facebook')
        except:
            facebook_login = None
        context = {'request': request, 'user': request.user, 'facebook_login': facebook_login}
        context.update(csrf(request))        
        return render_to_response('mainPage.html', context)        

def get_facebook_data(request):
    social_user = request.user.social_auth.filter(provider='facebook',).first()
    if social_user:
        url = u'https://graph.facebook.com/{0}/' \
              u'friends?fields=id,name,location,picture' \
              u'&access_token={1}'.format(
                  social_user.uid,
                  social_user.extra_data['access_token'],
              )
        url = u'https://graph.facebook.com/{0}/' \
              u'likes?access_token={1}'.format(
                  social_user.uid,
                  social_user.extra_data['access_token'],
              )
        #url = 'https://graph.facebook.com/v2.5/me/friends?access_token='+social_user.extra_data['access_token']
        print url
        res = requests.get(url)
        print res.text
        '''request = urllib2.Request(url)
        friends = json.loads(urllib2.urlopen(request).read()).get('data')
        print friends'''
        #for friend in friends:
    return redirect('/')