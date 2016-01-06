import webbrowser
import httplib2

__author__ = 'evangelie'
import os
from django.http import HttpResponse
from django.template.context import RequestContext
import requests
from django.shortcuts import render, redirect, render_to_response
from optimum.twitter import get_tweets
from optimum.personality import get_profil
import json
from pprint import pprint
from social_auth.models import UserSocialAuth
from apiclient.discovery import build


import datetime
from django.conf import settings
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI
from oauth2client.client import OAuth2Credentials, _extract_id_token
from oauth2client.django_orm import Storage

# Home page
def index(request):
    if request.method == 'GET':
        print request.user

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
        instance = UserSocialAuth.objects.filter(provider='google-oauth2').get()
        pprint(instance.tokens)
        print instance.tokens
        print instance.tokens['access_token']

        #r = requests.get('https://www.googleapis.com/drive/v2/files?key='+instance.tokens['access_token'])
        #print r.text
        '''response = requests.get(
            'https://www.googleapis.com/drive/v2/files',
            params={'access_token': instance.tokens['access_token']}
        )
        friends = response.text
        print friends'''
        #token_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(instance.tokens['expires_in']))
        #id_token = _extract_id_token(instance.tokens['id_token'])

        flow = flow_from_clientsecrets('optimum\static\json\json_credentials.json',
                               scope='https://www.googleapis.com/auth/drive',
                               redirect_uri='http://127.0.0.1:8000/')
        auth_uri = flow.step1_get_authorize_url()
        print auth_uri
        #credentials = flow.step2_exchange(instance.tokens['access_token'])
        '''state = 'b1Q8KgLwLilKyyMXuAN5iVy1ciQb2QY4'
        code = '4/s1H89dP9n_mfMnwmKp7evHM5001uB_w5zydkkSKUQoo'
        credentials = get_credentials(code, state)
        service = build_service(credentials)
        files = service.files.list.files().list().execute()
        about = service.about().get().execute()

        print 'Current user name: %s' % about['name']
        print 'Root folder ID: %s' % about['rootFolderId']
        print 'Total quota (bytes): %s' % about['quotaBytesTotal']
        print 'Used quota (bytes): %s' % about['quotaBytesUsed']'''

        #return render(request, "mainPage.html",)
        if request.GET.get('code'):
            code = request.GET.get('code')
            print code
            credentials = flow.step2_exchange(code)
            print credentials
            service = build_service(credentials)
            #files = service.files.list.files().list().execute()
            #print files
            result = retrieve_all_files(service)
            print result
            return render(request, "mainPage.html",)
        else:
            return redirect(auth_uri)
        #import pdb;pdb.set_trace()
        #return render(request, "mainPage.html")


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

import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient.discovery import build
from apiclient import errors
# ...


# Path to client_secret.json which should contain a JSON document such as:
#   {
#     "web": {
#       "client_id": "[[YOUR_CLIENT_ID]]",
#       "client_secret": "[[YOUR_CLIENT_SECRET]]",
#       "redirect_uris": [],
#       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#       "token_uri": "https://accounts.google.com/o/oauth2/token"
#     }
#   }
CLIENTSECRET_LOCATION = 'optimum\static\json\json_credentials.json'
REDIRECT_URI = '<YOUR_REGISTERED_REDIRECT_URI>'
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'email',
    'profile',
    # Add other requested scopes.
]

class GetCredentialsException(Exception):
  """Error raised when an error occurred while retrieving credentials.

  Attributes:
    authorization_url: Authorization URL to redirect the user to in order to
                       request offline access.
  """

  def __init__(self, authorization_url):
    """Construct a GetCredentialsException."""
    self.authorization_url = authorization_url


class CodeExchangeException(GetCredentialsException):
  """Error raised when a code exchange has failed."""


class NoRefreshTokenException(GetCredentialsException):
  """Error raised when no refresh token has been found."""


class NoUserIdException(Exception):
  """Error raised when no user ID could be retrieved."""


def get_stored_credentials(user_id):
  """Retrieved stored credentials for the provided user ID.

  Args:
    user_id: User's ID.
  Returns:
    Stored oauth2client.client.OAuth2Credentials if found, None otherwise.
  Raises:
    NotImplemented: This function has not been implemented.
  """
  # TODO: Implement this function to work with your database.
  #       To instantiate an OAuth2Credentials instance from a Json
  #       representation, use the oauth2client.client.Credentials.new_from_json
  #       class method.
  raise NotImplementedError()


def store_credentials(user_id, credentials):
  """Store OAuth 2.0 credentials in the application's database.

  This function stores the provided OAuth 2.0 credentials using the user ID as
  key.

  Args:
    user_id: User's ID.
    credentials: OAuth 2.0 credentials to store.
  Raises:
    NotImplemented: This function has not been implemented.
  """
  # TODO: Implement this function to work with your database.
  #       To retrieve a Json representation of the credentials instance, call the
  #       credentials.to_json() method.
  raise NotImplementedError()


def exchange_code(authorization_code):
  """Exchange an authorization code for OAuth 2.0 credentials.

  Args:
    authorization_code: Authorization code to exchange for OAuth 2.0
                        credentials.
  Returns:
    oauth2client.client.OAuth2Credentials instance.
  Raises:
    CodeExchangeException: an error occurred.
  """
  flow = flow_from_clientsecrets(CLIENTSECRET_LOCATION, ' '.join(SCOPES))
  flow.redirect_uri = REDIRECT_URI
  try:
    credentials = flow.step2_exchange(authorization_code)
    return credentials
  except FlowExchangeError, error:
    logging.error('An error occurred: %s', error)
    raise CodeExchangeException(None)


def get_user_info(credentials):
  """Send a request to the UserInfo API to retrieve the user's information.

  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
  user_info_service = build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except errors.HttpError, e:
    logging.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    return user_info
  else:
    raise NoUserIdException()


def get_authorization_url(email_address, state):
  """Retrieve the authorization URL.

  Args:
    email_address: User's e-mail address.
    state: State for the authorization URL.
  Returns:
    Authorization URL to redirect the user to.
  """
  flow = flow_from_clientsecrets(CLIENTSECRET_LOCATION, ' '.join(SCOPES))
  flow.params['access_type'] = 'offline'
  flow.params['approval_prompt'] = 'force'
  flow.params['user_id'] = email_address
  flow.params['state'] = state
  return flow.step1_get_authorize_url(REDIRECT_URI)


def get_credentials(authorization_code, state):
  """Retrieve credentials using the provided authorization code.

  This function exchanges the authorization code for an access token and queries
  the UserInfo API to retrieve the user's e-mail address.
  If a refresh token has been retrieved along with an access token, it is stored
  in the application database using the user's e-mail address as key.
  If no refresh token has been retrieved, the function checks in the application
  database for one and returns it if found or raises a NoRefreshTokenException
  with the authorization URL to redirect the user to.

  Args:
    authorization_code: Authorization code to use to retrieve an access token.
    state: State to set to the authorization URL in case of error.
  Returns:
    oauth2client.client.OAuth2Credentials instance containing an access and
    refresh token.
  Raises:
    CodeExchangeError: Could not exchange the authorization code.
    NoRefreshTokenException: No refresh token could be retrieved from the
                             available sources.
  """
  email_address = ''
  try:
    credentials = exchange_code(authorization_code)
    user_info = get_user_info(credentials)
    email_address = user_info.get('email')
    user_id = user_info.get('id')
    if credentials.refresh_token is not None:
      store_credentials(user_id, credentials)
      return credentials
    else:
      credentials = get_stored_credentials(user_id)
      if credentials and credentials.refresh_token is not None:
        return credentials
  except CodeExchangeException, error:
    logging.error('An error occurred during code exchange.')
    # Drive apps should try to retrieve the user and credentials for the current
    # session.
    # If none is available, redirect the user to the authorization URL.
    error.authorization_url = get_authorization_url(email_address, state)
    raise error
  except NoUserIdException:
    logging.error('No user ID could be retrieved.')
  # No refresh token has been retrieved.
  authorization_url = get_authorization_url(email_address, state)
  raise NoRefreshTokenException(authorization_url)


# ...

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

