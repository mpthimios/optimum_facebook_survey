import os
from django.http import HttpResponse

__author__ = 'evangelie'
from django.shortcuts import render, redirect, render_to_response
from optimum.twitter import get_tweets
from optimum.personality import get_profil
import json

# Home page
def index(request):
    if request.method == 'GET':
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
        return render(request, "map.html" )

