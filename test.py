from os import environ
import eventbrite
from flask import Flask, render_template, request
import pusher
import sys
import json
from pprint import pprint
import requests
import datetime

auth_token = environ['EVENTBRITE_OAUTH_TOKEN']
pusher_app_id = environ['PUSHER_APP_ID']
pusher_key = environ['PUSHER_KEY']
pusher_secret = environ['PUSHER_SECRET']

# Instantiate the Eventbrite API client.
eventbrite = eventbrite.Eventbrite(auth_token)

#Instantiate the pusher object. The pusher library pushes actions to the browser
# when they occur. 
p = pusher.Pusher(app_id=pusher_app_id, key=pusher_key, secret=pusher_secret)

def get_event_list():
    # Get today's date
    today = datetime.datetime.today()
    # Get the day of the week where Monday = 1
    weekday = today.isoweek.day()
    
