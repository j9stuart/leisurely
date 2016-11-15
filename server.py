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
from model import connect_to_db, db, Category, Weekday, WeekdayCategory, Activity, User
import meetup.api
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
from bcrypt import hashpw, gensalt
import geocoder

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
    category_list = random.sample(category_list, 5) 
    weekday = weekday.name


    return render_template("homepage.html", 
                            category_list=category_list, 
                            weekday=weekday)

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
    user_obj = User.query.filter_by(email=email).all()
    user = user_obj[0]
    user_password = user.password.encode('utf-8')
        
    if user == []:
        flash("No account associated with this email address. Please create an account below.")
        return redirect('/sign-up')
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
        user = User.query.filter_by(user=user_id).all()
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
    user = User.query.filter_by(email=email).all()

    if not user:
        password = password.encode('utf-8')
        password = hashpw(password, gensalt())
        print password
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Congratulations! You successfully created an account!")
    else:
        flash("An account with this email address already exists!")

    return redirect("/")


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
        activity_list[activity_name] = activity.act_id

    return jsonify(activity_list)

# ------------------------------------------------------------- #

@app.route('/event-list')
def show_event_list():
    """This displays a list of events"""
    # Get data from browser to find user location and activity information
    location = request.args.get('location')
    act_id = request.args.get('act_id')
    locate = geocoder.google(location)
    lat, lng = locate.latlng
    
    activity = Activity.query.filter_by(act_id=act_id).one()
    eb_cat_id = activity.eb_cat_id
    eb_format_id = activity.eb_format_id
    eb_sub_id = activity.sub_cat
    mu_id = activity.mu_id
    event_details = [] 

    # Get datetime to use in api query
    now = datetime.datetime.now()
    endtime = now.strftime("%Y-%m-%d 23:59:59")

    if location is None or locate == []:
        flash("The location you entered could not be found. Please try your search again.")
        return redirect("")

    if mu_id != 0:
        events = meetup.GetOpenEvents(category=mu_id, lat=lat, lon=lng)
        for event in events.results:
            event_name = event.get("name")
            event_url = event.get("event_url")
            event_photo = event.get("photo_url")
            event_deets = [event_name, event_url, event_photo]
            event_details.append(event_deets)

        return render_template("meetup_events.html",
                                event_details=event_details)

    else:
        if eb_sub_id != str(0):
            events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&subcategories="+eb_sub_id+"&location.latitude="+str(lat)+"&location.longitude="+str(lng))
        else:
            events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&formats="+str(eb_format_id)+"&location.latitude="+str(lat)+"&location.longitude="+str(lng))

        if events.get("events") == [] or events.get("events") is None:
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


# ------------------------------------------------------------- #

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = True
    connect_to_db(app)

    DebugToolbarExtension(app)
    app.run(host='0.0.0.0', debug=True)