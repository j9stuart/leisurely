from os import environ
import eventbrite
from flask import Flask, render_template, request, jsonify, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import pusher
import sys
import json
from pprint import pprint
import requests
from jinja2 import StrictUndefined
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

app = Flask(__name__)
app.debug = True
app.jinja_env.undefined = StrictUndefined
app.secret_key = "leisure"


def get_event_list():
    event = eventbrite.get('/categories')
    event = event.pretty
    print event


@app.route('/')
def index():
    """This the app homepage view"""



    return render_template("homepage.html")

@app.route('/event-list')
def show_event_list():
    """This displays a list of events"""

    #Get event details
    event = eventbrite.get('/categories')
    return event

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = True

    DebugToolbarExtension(app)
    app.run(host='0.0.0.0', debug=True)