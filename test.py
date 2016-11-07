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
    
    category_list = {}
    activity_list = []
    # Get today's date
    weekday = datetime.datetime.today().isoweekday()
    # Get the day of the week where Monday = 1
    # Query database to get weekday categories and their associated activities
    weekday = Weekday.query.get(weekday)
    for category in weekday.categories:
        category_name = category.screenname
        activities = Category.query.filter_by(screenname=category_name).one().activities
        for activity in activities:
            activity_list.append(activity.name)
        category_list[category_name] = activity_list
        activity_list = []

    # Generate a random list of 5 categories to dispaly from dictionary
    c1, c2, c3, c4, c5 = random.sample(category_list.items(), 5) 
    weekday = weekday.name
    category_json = json.dumps(category_list)


    return render_template("homepage.html", 
                            c1=c1, c2=c2,
                            c3=c3, c4=c4, c5=c5, weekday=weekday, category_json=category_json)