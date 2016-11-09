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
import meetup.api

auth_token = environ['EVENTBRITE_OAUTH_TOKEN']
pusher_app_id = environ['PUSHER_APP_ID']
pusher_key = environ['PUSHER_KEY']
pusher_secret = environ['PUSHER_SECRET']
mu_token = environ['MEETUP_API_KEY']

# Instantiate the Eventbrite and Meetup API clients.
eventbrite = eventbrite.Eventbrite(auth_token)
meetup = meetup.api.Client(mu_token)

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
    category_list = []
       # Get today's date
    weekday = datetime.datetime.today().isoweekday()
    # Get the day of the week where Monday = 1
    # Query database to get weekday categories and their associated activities
    weekday = Weekday.query.get(weekday)
    for category in weekday.categories:
        category_name = category.screenname
        category_list.append(category_name)

    # Generate a random list of 5 categories to dispaly from dictionary
    c1, c2, c3, c4, c5 = random.sample(category_list, 5) 
    weekday = weekday.name


    return render_template("homepage.html", 
                            c1=c1, c2=c2,
                            c3=c3, c4=c4, c5=c5, 
                            weekday=weekday)



@app.route("/activities.json")
def show_activities():
    """This displays a list of activities based on the user selected category"""

    screenname = request.args.get('category')
    # Query database to get category in order to get activities
    category = Category.query.filter_by(screenname=screenname).one()
    activity_list = {}
    for activity in category.activities:
        activity_name = activity.name
        activity_list[activity_name] = activity.act_id

    return jsonify(activity_list)



@app.route('/event-list')
def show_event_list():
    """This displays a list of events"""
    # Get data from browser
    act_id = request.args.get('category')
    activity = Activity.query.filter_by(act_id=act_id).one()
    eb_cat_id = activity.eb_cat_id
    eb_format_id = activity.eb_format_id
    eb_sub_id = activity.sub_cat
    mu_id = activity.mu_id
    event_details = []

    print act_id
    print eb_cat_id
    print eb_format_id
    print eb_sub_id 
    print mu_id   

    if mu_id != 0:
        events = meetup.GetOpenEvents(category=mu_id, zip=94122)
        for event in events.results:
            event_name = event.get("name")
            event_url = event.get("event_url")
            event_deets = (event_name, event_url)
            event_details.append(event_deets)

        return render_template("meetup_events.html",
                                event_details=event_details)

    else:
        if eb_sub_id != str(0):
            events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&subcategories="+eb_sub_id)
        else:
            events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&formats="+str(eb_format_id))

        print pprint(events)

        if events.get("events") == []:
            flash('Sorry there are no events at this time!')
            return redirect("/")

        else:
            event_list = events.get("events")
            for event in event_list:
                event_name_dict = event.get("name")
                event_name = event_name_dict.get("text")
                event_url = event.get("url")
                event_deets = (event_name, event_url)
                event_details.append(event_deets)
    
            return render_template("eventbevents.html",
                                event_details=event_details)




if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = True
    connect_to_db(app)

    DebugToolbarExtension(app)
    app.run(host='0.0.0.0', debug=True)