__author__ = 'evangelie'
import requests
import json

def get_profil(all_tweets):
    # Local variables
    url = "https://gateway.watsonplatform.net/personality-insights/api"
    username = "5956e74e-9bc7-4185-a4a3-201824a21d4c"
    password = "Wlll5HZjVs6M"
    response = requests.post(url + "/v2/profile",
                        auth=(username,password),
                        headers = {"content-type": "text/plain"},
                        data=json.dumps(all_tweets)
                        )
    return response