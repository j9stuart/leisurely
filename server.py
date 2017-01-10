from bcrypt import hashpw, gensalt
import datetime
import eventbrite
from flask import Flask, render_template, request, jsonify, redirect, flash, session
from flask_compress import Compress
from flask_debugtoolbar import DebugToolbarExtension
from functions import is_email_address_valid, check_password, query_eb_subcat, query_eb_formats, get_filter_value, query_mu
import geocoder
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
from jinja2 import StrictUndefined
import json
import meetup.api
from model import connect_to_db, db, Category, Weekday, WeekdayCategory, Activity, User, SavedEvent, SearchInfo
from os import environ
from pprint import pprint
import random
import re
import requests
import sys

auth_token = environ['EVENTBRITE_OAUTH_TOKEN']
pusher_app_id = environ['PUSHER_APP_ID']
pusher_key = environ['PUSHER_KEY']
pusher_secret = environ['PUSHER_SECRET']
mu_token = environ['MEETUP_API_KEY']
geo_code = environ['GEOCODE_API_KEY']

# Instantiate the Eventbrite and Meetup API clients.
eventbrite = eventbrite.Eventbrite(auth_token)
meetup = meetup.api.Client(mu_token)
google_maps = GoogleMaps(api_key=geo_code)
geo_api = geo_code
compress = Compress()

app = Flask(__name__)
Compress(app)
app.debug = False
app.jinja_env.undefined = StrictUndefined
app.secret_key = "leisure"

MEETUP_IMG_URL = "static/assets/meetup_logo.png"
EVBRTE_IMG_URL = "static/assets/eb_logo.jpg"


# ----------------------------- ROUTES ---------------------------------- #


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
        category_pic = category.img_url
        category_list.append((category_name, category_pic))

    # Generate a random list of 5 categories to display from dictionary based on weekday
    category_list = random.sample(category_list, 5) 
    weekday = weekday.name


    return render_template("homepage.html", 
                            category_list=category_list, 
                            weekday=weekday, geo_api=geo_api)

# ------------------------------------------------------------- #

@app.route('/sign-in')
def sign_in():

    return render_template("sign_in.html")

# ------------------------------------------------------------- #

@app.route('/submit-signin', methods=['POST'])
def submit_form():
    """Submits sign-in information"""

    email = request.form.get('email')
    password = request.form.get('password').encode('utf-8')
    if not is_email_address_valid(email):
        flash("Please enter a valid email address")
        return redirect("/sign-in")

    user_obj = User.query.filter_by(email=email).all()

    if user_obj == []:
        flash("No account associated with this email address. Please create an account below.")
        return redirect('/sign-up')

    user = user_obj[0]
    user_password = user.password.encode('utf-8')

    if user_password == hashpw(password, user_password):
        user_id = user.user_id
        session["user_id"] = user_id
        flash('You were successfully logged in')
        return redirect("/user-profile")
    else:
        flash('Invalid credentials')
        return redirect('/sign-in')

# ------------------------------------------------------------- #

@app.route('/user-profile')
def show_user_info():
    """Show user-specific information"""
    if session == {}:
        return redirect("/")
    else:
        user = session['user_id']
        user = User.query.filter_by(user_id=user).all()
        user = user[0]
        email = user.email


    return render_template("user_profile.html", 
                            email=email)

# ------------------------------------------------------------- #

@app.route('/sign-up')
def create_user():
    """Render a form for user to create account"""

    return render_template("sign_up.html")


# ------------------------------------------------------------- #


@app.route('/submit-signup', methods=["POST"])
def submit_account():
    """Get email and password, sign-in (if exist), or create new user"""

    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    user = User.query.filter_by(email=email).all()

    if not is_email_address_valid(email):
        flash("Please enter a valid email address")
        return redirect("/sign-up")       
    if check_password(password):
        if not user:
            password = password.encode('utf-8')
            password = hashpw(password, gensalt())
            new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)
            db.session.add(new_user)
            db.session.commit()
            flash("Congratulations! You successfully created an account!")
        else:
            flash("An account with this email address already exists!")
        return redirect("/")
    else:
        return redirect("/sign-up")    


# ------------------------------------------------------------- #

@app.route('/sign-out')
def log_out():
    """Logs user out"""

    del session["user_id"]
    flash('You were successfully logged out')
    return redirect("/")

# ------------------------------------------------------------- #

@app.route("/activities.json")
def show_activities():
    """This displays a list of activities based on the user selected category"""

    screenname = request.args.get('category')
    # Query database to get category in order to get activities
    category = Category.query.filter_by(screenname=screenname).one()
    activity_list = {}
    for activity in category.activities:
        activity_name = activity.name
        img_url = activity.img_url
        activity_list[activity_name] = [activity.act_id, img_url]

    return jsonify(activity_list)

# ------------------------------------------------------------- #

@app.route('/event-list')
def show_event_list():
    """This displays a list of events"""
    # Get data from browser to find user location and activity information
    location = request.args.get('location')
    act_id = request.args.get('act_id')
    filter_by = request.args.get('filter')
    locate = geocoder.google(location)
    city = locate.city
    if location is "" or locate.city is None:
        flash("The location you entered could not be found. Please try your search again.")
        return redirect("/")
    lat, lon = locate.latlng
    
    activity = Activity.query.filter_by(act_id=act_id).one()
    eb_cat_id = activity.eb_cat_id
    eb_format_id = activity.eb_format_id
    eb_sub_id = activity.sub_cat
    mu_id = activity.mu_id
    event_details = [] 

    # Get datetime to use in api query
    now = datetime.datetime.now()

    # ---------------------- DATABASE SAVE SEARCH QUERY ----------------------#

    new_search = SearchInfo(cat_id=activity.category.cat_id, act_id=act_id, filter_by=filter_by, city=city, datetime=now)
    db.session.add(new_search)
    db.session.commit()
    result_code = 'Add'

    # ---------------------- FUNCTION CONTINUES BELOW ----------------------#
     
    if mu_id != 0:
        events = query_mu(mu_id, lat, lon, filter_by)
        
        if events.results is None:
            flash('Sorry there are no events for your search at this time!')
            return redirect("/")
        else:
            for event in events.results:
                event_name = event.get("name")
                event_url = event.get("event_url")
                event_img = event.get("group").get("group_photo", {"photo_link": MEETUP_IMG_URL}).get("photo_link", MEETUP_IMG_URL)
                event_id = event.get("id")

                event_deets = [event_name, event_url, event_img, event_id]
                event_details.append(event_deets)

        return render_template("meetup_events.html",
                                event_details=event_details)

    else:
        filter_value = get_filter_value(filter_by)

        if eb_sub_id != str(0):
            events = query_eb_subcat(eb_cat_id, filter_value, eb_sub_id, location)
            
        else:
            events = query_eb_formats(eb_cat_id, filter_value, eb_format_id, location)

        if events.get("events") == [] or events.get("events") is None:
            flash('Sorry there are no events at this time!')
            return redirect("/")

        else:
            event_list = events.get("events")
            for event in event_list:
                event_name = event.get("name").get("text")
                event_url = event.get("url")
                event_img = event.get("logo")
                if event_img is None:
                    event_img = EVBRTE_IMG_URL
                else:
                    event_img = event_img.get("original", {}).get("url", EVBRTE_IMG_URL)
                event_id = event.get("id")
                
                event_deets = [event_name, event_url, event_img, event_id]
                event_details.append(event_deets)

            return render_template("eventbevents.html",
                                event_details=event_details)


# --------------------------------------------------------------------------- #

@app.route("/save_event.json", methods=["POST"])
def save_event():
    """Saves an event to a saved events page for users"""

    event_id = int(request.form.get("event_id"))
    event_name = request.form.get("event_name")
    event_url = request.form.get("event_url")
    user_id = int(session["user_id"])
    event_pic = request.form.get("event_pic")
    print event_pic

    old_saved_event = SavedEvent.query.filter(SavedEvent.event_id == event_id, SavedEvent.user_id == user_id).all()

    print old_saved_event

    if old_saved_event: 
        db.session.delete(old_saved_event[0])
        db.session.commit()
        result_code = 'Delete'
        print "deleted" 

    else:
        new_saved_event = SavedEvent(user_id=user_id, event_id=event_id, event_name=event_name, event_url=event_url, event_pic=event_pic)
        db.session.add(new_saved_event)
        db.session.commit()
        result_code = 'Add'
        print "added"
    
    return jsonify({'code': result_code})


# ------------------------------------------------------------- #

@app.route("/saved-events")
def show_saved_events():
    """Shows the user events they have saved"""

    user_id = session["user_id"]
    saved_events = SavedEvent.query.filter_by(user_id=user_id).all()

    return render_template("saved_events.html", saved_events=saved_events)


# ------------------------------------------------------------- #


if __name__ == "__main__":
    app.debug = False
    app.jinja_env.auto_reload = True
    connect_to_db(app)

    DebugToolbarExtension(app)
    app.run(host='0.0.0.0')