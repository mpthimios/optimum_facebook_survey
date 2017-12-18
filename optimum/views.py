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
from django.http import HttpResponse, HttpResponseRedirect
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
import random

# Home page
def index(request):
  if request.method == 'GET':
    lang = "en"
    try: 
      print request.GET.get('lang')
      if (request.GET.get('lang') != None):
        if (request.GET.get('lang') == "de"):
          lang = "de"
    except:
      print "lang not available"

    context = {'lang' : lang}    
    return render(request, 'mainPage.html', context)

def facebook_connect(request):
    if request.method == 'POST':
        print "POST"
        #http://survey.tech-experience.at/index.php/943719/lang-en
        #referer = request.META.get('HTTP_REFERER')
        #request.session['referer'] = ""
        #referer_url_present = None
        #if (referer != None and referer.find("survey.tech-experience.at") >=0):        
        #  request.session['referer'] = request.META.get('HTTP_REFERER')
        #if (request.session['referer'] != ""):
        #  referer_url_present = "present"
        #session_referer = request.META.get('HTTP_REFERER')

        url_lang = "lang-en"
        lang = (request.POST.get('lang', ''))
        if (lang == "de"):
          url_lang = "lang-de"
        
        print url_lang
        request.session['lang'] = url_lang

        random_user_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        print random_user_id
        referer_url = ''
        facebook_login = None        
        try:
          facebook_login = request.user.social_auth.get(provider='facebook')
          try:
            random_user_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
            print random_user_id
            get_facebook_data(request, random_user_id)            
            referer_url = "http://survey.tech-experience.at/index.php/943719/" + url_lang + "?accessFBdata1=" + random_user_id + "&newtest=Y"
          except:
            print "could not get facebook data"
            traceback.print_exc()
        except:
          print "user is not authenticated"      
        context = {'request': request, 'user': request.user, 'facebook_login': facebook_login, 'referer': referer_url, 'lang': url_lang}
        context.update(csrf(request))        
        return render_to_response('facebookPage.html', context)
    else:
        print "GET"
        url_lang = "lang-en"
        if (request.session['lang'] != None):
          url_lang = request.session['lang']
        print url_lang
        referer_url = ''
        facebook_login = None        
        try:
          facebook_login = request.user.social_auth.get(provider='facebook')
          try:
            random_user_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
            print random_user_id
            get_facebook_data(request, random_user_id)            
            referer_url = "http://survey.tech-experience.at/index.php/943719/" + url_lang + "?accessFBdata1=" + random_user_id + "&newtest=Y"
          except:
            print "could not get facebook data"
            traceback.print_exc()
        except:
          print "user is not authenticated"      
        context = {'request': request, 'user': request.user, 'facebook_login': facebook_login, 'referer': referer_url, 'lang': url_lang}
        context.update(csrf(request))        
        return render_to_response('facebookPage.html', context)

def facebook_disconnect(request):
    if request.method == 'GET':
        print "how to handle this"
        facebook_login = None        
        try:
          facebook_login = request.user.social_auth.get(provider='facebook')
        except:
          print "user is not authenticated"      
        context = {'request': request, 'user': request.user, 'facebook_login': facebook_login} 
        context.update(csrf(request))
        return render_to_response('facebookDisconnectPage.html', context)

def survey_redirect(request):
    redirect_url = request.GET["next"]
    print redirect_url
    return HttpResponseRedirect(redirect_url)

def get_facebook_data(request, random_user_id):
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
        new_user_data = UserFacebookData.objects.create(user = social_user, likes=likes, tagged_photos=tagged_photos, uploaded_photos=uploaded_photos, posts=posts, random_id=random_user_id)        
    else:
        user_data = UserFacebookData.objects.get(user=social_user)
    return True

