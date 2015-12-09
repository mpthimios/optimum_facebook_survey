__author__ = 'evangelie'

import tweepy
from tweepy import OAuthHandler
import json


def get_tweets():

    consumer_key = 'm69DRR5qxEl8DDYzmNkOgI3dX'
    consumer_secret = 'gHtJr6z7qlJxBI6XqWJ8NTi9kAQxpFJ0TKSlBSR0vnSMGSOYY4'
    access_token = '4338168808-i35fTxake2n6JkffdyaBqHUGGPLryZjgPpVlzmw'
    access_secret = 'ikaAZp2EJVEc4kXhNi23cEBv3FoipTTIpf1uxBVW3cEKc'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    all_tweets = []

    for tweets in tweepy.Cursor(api.user_timeline, screen_name="imu_ntua", lang="en", include_rts="false").items(1000):
            if tweets.lang == 'en':
                all_tweets.append(tweets.text)

    return json.dumps(all_tweets)
