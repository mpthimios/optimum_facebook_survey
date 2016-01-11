import json
from oauth2client.client import OAuth2Credentials
from datetime import datetime

__author__ = 'evangelie'


def creds_to_json(credentials):
    """
    :param credentials: The Google api credentials
    :return: A json string describing the credentials
    """
    #print credentials['scopes']
    print credentials.scopes
    c = {
        'scopes': list(credentials.scopes)[0],
        'revoke_uri': credentials.revoke_uri,
        'access_token': credentials.access_token,
        'token_uri': credentials.token_uri,
        'token_info_uri': credentials.token_info_uri,
        #'refresh_token': credentials.refresh_token,
        #'token_response': credentials.token_response,
        'token_type': credentials.token_response['token_type'],
        'expires_in': credentials.token_response['expires_in'],
        'refresh_token': credentials.token_response['refresh_token'],
        'invalid': credentials.invalid,
        'client_id': credentials.client_id,
        'id_token': credentials.id_token,
        'client_secret': credentials.client_secret,
        'token_expiry': credentials.token_expiry,
        'store': credentials.store,
        'user_agent': credentials.user_agent
    }
    return json.dumps(c, default=json_serial)
    #return  json.dumps(c)
def creds_from_json(j_str):
    """
    :param j_str: json string containing credentials information
    :return: an OAuth2Credentials instance
    """
    c = json.loads(j_str)
    token_response = {
        'token_type': c['token_type'],
        'expires_in': c['expires_in'],
        'refresh_token' : c['refresh_token']
    }
    creds = OAuth2Credentials(c['access_token'], c['client_id'], c['client_secret'], c['refresh_token'],  c['token_expiry'], c['token_uri'],c['user_agent'], c['revoke_uri'], c['id_token'], token_response  )
    '''creds.scopes = set([c['scopes']])
    creds.revoke_uri  = c['revoke_uri']
    creds.access_token = c['access_token']
    creds.token_uri = c['token_uri']
    creds.token_info_uri = c['token_info_uri']
    #creds.token_response = c['token_response']
    creds.token_response = {
        'token_type': c['token_type'],
        'expires_in': c['expires_in'],
        'refresh_token' : c['refresh_token']
    }
    creds.invalid = c['invalid']
    creds.client_id = c['client_id']
    creds.id_token = c['id_token']
    creds.client_secret = c['client_secret']
    creds.token_expiry = c['token_expiry']
    creds.store = c['store']
    creds.user_agent = c['user_agent']'''
    return creds

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")