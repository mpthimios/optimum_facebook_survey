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
from social_auth.db.django_models import UserSocialAuth
from apiclient.discovery import build
import oauth2client
from oauth2client import client
from oauth2client import tools
import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors


import datetime
from django.conf import settings
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI
from oauth2client.client import OAuth2Credentials, _extract_id_token
from oauth2client.django_orm import Storage
from gcm import*

# Home page
def index(request):
    if request.method == 'GET':
        if not request.user:
            return redirect('/accounts/login')

        #Get all tweets of user written in English
        #all_tweets = get_tweets()
        #print all_tweets
        #Get Big 5 personality using IBM watson API
        '''response = get_profil(all_tweets)
        try:
            print json.loads(response.text)
            personality = json.loads(response.text)

        except:
            raise Exception("Error processing the request, HTTP: %d" % response.status_code)'''
        data = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'optimum/static/files/new_2.gpx'), 'r')
        #return render(request, "map.html" )
        if request.is_ajax():
            data = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'optimum/static/files/new_2.gpx'), 'r')
            #data= open('/static/files/new.gpx', 'r')
            #origin lat="38.059016" lon="23.755915"
            #dest lat="38.012388" lon="23.637945"
            return HttpResponse(data)

        return render(request, "mainPage.html",)

def history_routes(request):
    if request.method == 'GET':

        data = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'optimum/static/files/new_2.gpx'), 'r')
        #return render(request, "map.html" )
        if request.is_ajax():
            data = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'optimum/static/files/new_2.gpx'), 'r')
            #data= open('/static/files/new.gpx', 'r')
            #origin lat="38.059016" lon="23.755915"
            #dest lat="38.012388" lon="23.637945"
            return HttpResponse(data)

        return render(request, "map.html")

def tracks(request):
    if request.method == 'GET':
        instance = UserSocialAuth.objects.filter(provider='google-oauth2').get()
        pprint(instance.tokens)
        print instance.tokens
        print instance.tokens['access_token']
        '''flow = flow_from_clientsecrets('optimum\static\json\json_credentials.json',
                               scope='https://www.googleapis.com/auth/drive',
                               redirect_uri='http://127.0.0.1:8000/')

        auth_uri = flow.step1_get_authorize_url()
        print auth_uri
        user = UserSocialAuth.objects.get(provider='google-oauth2')
        print user.user
        UserCredentials.objects.filter(id=11).delete()
        q = UserCredentials.objects.filter(user=user.user)

        if not q:
            if request.GET.get('code'):
                code = request.GET.get('code')
                request.session['code'] = code
                credentials = flow.step2_exchange(code)
                cred = UserCredentials.objects.create(user=user.user, credentials=creds_to_json(credentials))
                service = build_service(credentials)
                #files = service.files.list.files().list().execute()
                #print files
                result = retrieve_all_files(service)
                print result
                return render(request, "mainPage.html",)
            else:
                return redirect(auth_uri)
        else:

            cred = UserCredentials.objects.get(user=user.user)
            print cred.id
            code = request.session.get('code', '')
            print code
            credentials = creds_from_json(cred.credentials)
            #import pdb;pdb.set_trace()


            service = build_service(credentials)'''
    service= get_service(request)
    result = retrieve_all_files(service)
    print result
    return render(request, "tracks.html", {'result': result} )

def path(request):
    if request.method == 'GET':
        file=request.GET.get('file')
        '''flow = flow_from_clientsecrets('optimum\static\json\json_credentials.json',
                               scope='https://www.googleapis.com/auth/drive',
                               redirect_uri='http://127.0.0.1:8000/')

        auth_uri = flow.step1_get_authorize_url()
        print auth_uri
        user = UserSocialAuth.objects.get(provider='google-oauth2')
        q = UserCredentials.objects.filter(user=user.user)

        if not q:
            if request.GET.get('code'):
                code = request.GET.get('code')
                request.session['code'] = code
                credentials = flow.step2_exchange(code)
                cred = UserCredentials.objects.create(user=user.user, credentials=creds_to_json(credentials))
                service = build_service(credentials)
                return render(request, "mainPage.html",)
            else:
                return redirect(auth_uri)
        else:

            cred = UserCredentials.objects.get(user=user.user)
            print cred.id
            code = request.session.get('code', '')
            print code
            credentials = creds_from_json(cred.credentials)

            service = build_service(credentials)'''
        service = get_service(request)
        #data = get_file_content(service, file)
        if request.is_ajax():
            data = get_file_content(service, file)
            return HttpResponse(data)

        return render(request, "map.html")


def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      param['q'] = "fileExtension = 'gpx'"
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result

def build_service(credentials):
  """Build a Drive service object.

  Args:
    credentials: OAuth 2.0 credentials.

  Returns:
    Drive service object.
  """
  http = httplib2.Http()
  http = credentials.authorize(http)
  return build('drive', 'v2', http=http)


def get_file_content(service, file_id):
  """Get a file's content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file.

  Returns:
    File's content if successful, None otherwise.
  """
  try:
    return service.files().get_media(fileId=file_id).execute()
  except errors.HttpError, error:
    return 'An error occurred: %s' % error

def get_service(request):
        flow = flow_from_clientsecrets('optimum\static\json\json_credentials.json',
                               scope='https://www.googleapis.com/auth/drive',
                               redirect_uri='http://127.0.0.1:8000/')

        auth_uri = flow.step1_get_authorize_url()
        print auth_uri
        user = UserSocialAuth.objects.get(provider='google-oauth2')
        q = UserCredentials.objects.filter(user=user.user)

        if not q:
            if request.GET.get('code'):
                code = request.GET.get('code')
                request.session['code'] = code
                credentials = flow.step2_exchange(code)
                cred = UserCredentials.objects.create(user=user.user, credentials=creds_to_json(credentials))
                service = build_service(credentials)
                return service
            else:
                return redirect(auth_uri)
        else:

            cred = UserCredentials.objects.get(user=user.user)
            print cred.id
            code = request.session.get('code', '')
            print code
            credentials = creds_from_json(cred.credentials)

            service = build_service(credentials)

        return service

def send_notification(request):
    gcm = GCM("AIzaSyDejSxmynqJzzBdyrCS-IqMhp0BxiGWL1M")
    data = {'the_message': 'You have x new friends', 'param2': 'value2'}

    reg_id = 'APA91bHDRCRNIGHpOfxivgwQt6ZFK3isuW4aTUOFwMI9qJ6MGDpC3MlOWHtEoe8k6PAKo0H_g2gXhETDO1dDKKxgP5LGulZQxTeNZSwva7tsIL3pvfNksgl0wu1xGbHyQxp2CexeZDKEzvugwyB5hywqvT1-UxxxqpL4EUXTWOm0RXE5CrpMk'

    gcm.plaintext_request(registration_id=reg_id, data=data)
