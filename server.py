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
import random
from model import connect_to_db, db, Category, Weekday, WeekdayCategory, Activity

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


@app.route('/')
def index():
    """This the app homepage view"""

    # Get today's date
    today = datetime.datetime.today()
    # Get the day of the week where Monday = 1
    weekday = today.isoweekday()
    # Query database to get weekday categories
    weekday = Weekday.query.get(weekday)
    category_list = []
    for category in weekday.categories:
        category_name = category.screenname
        category_list.append(category_name)

    # Generate a random list of 5 categories from list
    c1, c2, c3, c4, c5 = random.sample(category_list, 5) 
    
    return render_template("homepage.html", 
                            c1=c1, c2=c2,
                            c3=c3, c4=c4, c5=c5)


@app.route('/activities', methods=["POST"])
def show_activities():
    """This displays a list of activities based on the user selected category"""

    screenname = request.form.get("category")
    # Query database to get category in order to get activities
    category = Category.query.filter_by(screenname=screenname).one()
    activity_list = []
    for activity in category.activities:
        activity_name = activity.name
        activity_list.append(activity_name)

    return activity_list


@app.route('/event-list')
def show_event_list():
    """This displays a list of events"""

    #Get event details
    event = eventbrite.get('/categories')
    event = event.pretty
    return event


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = True
    connect_to_db(app)

    DebugToolbarExtension(app)
    app.run(host='0.0.0.0', debug=True)