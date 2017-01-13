# Functions to be used for server file
from bcrypt import hashpw, gensalt
import datetime
import eventbrite
from flask import Flask, render_template, request, jsonify, redirect, flash, session
from flask_compress import Compress
from flask_debugtoolbar import DebugToolbarExtension
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
mu_token = environ['MEETUP_API_KEY']
geo_code = environ['GEOCODE_API_KEY']


# Instantiate the Eventbrite, GoogleMaps, and Meetup API clients.
eventbrite = eventbrite.Eventbrite(auth_token)
meetup = meetup.api.Client(mu_token)
google_maps = GoogleMaps(api_key=geo_code)
geo_api = geo_code

# Email Validation Check
EMAIL_VALIDATOR = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"

# Default Images for Eventbrite and Meetup events
MEETUP_IMG_URL = "static/assets/meetup_logo.png"
EVBRTE_IMG_URL = "static/assets/eb_logo.jpg"



def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match(EMAIL_VALIDATOR, email):
        return False
    return True


# --------------------------- FUNCTIONS --------------------------------- #


def check_password(password):
    """Validate the password by checking length"""
    if 6 <= len(password) < 12:
        return True
        
    else:
        flash('Your password must be between 6 and 12 characters. Please try again.')
        return False


# --------------------------- FUNCTIONS --------------------------------- #


def query_eb_subcat(eb_cat_id, filter_value, eb_sub_id, location):
    """Constructs the eventbrite query based on user selected filter"""
    if filter_value == 0:
        events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&subcategories="+eb_sub_id+"&location.address="+str(location))

    if filter_value == 4:
        events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&subcategories="+eb_sub_id+"&location.address="+str(location)+"price=free")

    else:
        events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&subcategories="+eb_sub_id+"&location.address="+str(location)+"start_date.keyword="+filter_value)

    return events


# --------------------------- FUNCTIONS --------------------------------- #



def query_eb_formats(eb_cat_id, filter_value, eb_format_id, location):
    """Constructs the eventbrite query based on user selected filter"""

    if filter_value == 0:
        events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&formats="+str(eb_format_id)+"&location.address="+str(location))

    if filter_value == 4:
        events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&formats="+str(eb_format_id)+"&location.address="+str(location)+"price=free")

    else:
        events = eventbrite.get("/events/search/?categories="+str(eb_cat_id)+"&formats="+str(eb_format_id)+"&location.address="+str(location)+"start_date.keyword="+filter_value)

    return events

# --------------------------- FUNCTIONS --------------------------------- #

def get_filter_value(filter_by):
    """ Takes value and returns a string version"""

    filter_value = ""

    if filter_by == 1:
        filter_value = "today"

    if filter_by == 2:
        filter_value = "this_week"

    if filter_by == 3:
        filter_value = "this_month"

    return filter_value

# --------------------------- FUNCTIONS --------------------------------- #

def query_mu(mu_id, lat, lon, filter_by):
    """ Constructs Meetup query based on user filters."""
    
    if filter_by == 1:
        events = meetup.GetOpenEvents(category=mu_id, lat=lat, lon=lon, time="1d", fields="group_photo")

    if filter_by == 2:
        events = meetup.GetOpenEvents(category=mu_id, lat=lat, lon=lon, time="1w", fields="group_photo")

    if filter_by == 3:
        events = meetup.GetOpenEvents(category=mu_id, lat=lat, lon=lon, time="1m", fields="group_photo")

    else:
        events = meetup.GetOpenEvents(category=mu_id, lat=lat, lon=lon, fields="group_photo")

    return events

# ----------------------------- FUNCTIONS ---------------------------------- #

def load_events():
    """Load events from eventbrite & meetup into database"""

    print "Events"

    Event.query.delete()

    event_details = seed_events("eventbrite")

    for line in event_details:
        event_name, event_url, event_img, source_event_id, description, start_time, eb_category_id, mu_category_id = line

        event = Event(event_name=event_name,
                      event_url=event_url,
                      event_img=event_img,
                      source_event_id=source_event_id,
                      description=description,
                      start_time=start_time,
                      eb_category_id=eb_category_id,
                      mu_category_id=mu_category_id,)

        db.session.add(event)

    event_details = seed_events("meetup")

    for line in event_details:
        event_name, event_url, event_img, source_event_id, description, start_time, eb_category_id, mu_category_id = line

        event = Event(event_name=event_name,
                      event_url=event_url,
                      event_img=event_img,
                      source_event_id=source_event_id,
                      description=description,
                      start_time=start_time,
                      eb_category_id=eb_category_id,
                      mu_category_id=mu_category_id,)
        
        db.session.add(event)

    db.session.commit()

# ----------------------------- FUNCTIONS ---------------------------------- #

def seed_events(source):
    """ Requests list of all eventbrite and meetup events for database entry """
    event_details = []
    i = 1

    if source == "eventbrite":
        while i <= 50:
            source = 1
            events = eventbrite.get("/events/search/?location.address=94102&page="+str(i))
            event_list = events.get("events")
            for event in event_list:
                event_name = event.get("name").get("text")
                event_url = event.get("url")
                event_img = event.get("logo")
                if event_img is None:
                    event_img = EVBRTE_IMG_URL
                else:
                    event_img = event_img.get("original", {}).get("url", EVBRTE_IMG_URL)

                source_event_id = event.get("id")
                description = event.get("description").get("text")
                uc_time = event.get("start").get("utc")
                time = datetime.datetime.strptime(uc_time, '%Y-%m-%dT%H:%M:%SZ')
                start_time = time.strftime('%Y-%m-%d %H:%M:%S')
                eb_category_id = event.get("category_id")
                # eb_category_id = 0
                mu_category_id = 0

                event_deets = [event_name, event_url, event_img, source_event_id, description, start_time, eb_category_id, mu_category_id]
                event_details.append(event_deets)
                i += 1
        print event_details
        return event_details


    if source == "meetup":
        source = 2
        events = meetup.GetOpenEvents(lat=37, lon=-122, fields="group_photo")
        for event in events.results:
            event_name = event.get("name")
            event_url = event.get("event_url")
            event_img = event.get("group").get("group_photo", {"photo_link": MEETUP_IMG_URL}).get("photo_link", MEETUP_IMG_URL)
            source_event_id = event.get("id")
            description = event.get("description")
            ms_time = event.get("time")
            time = datetime.datetime.fromtimestamp(ms_time/1000)
            start_time = time.strftime('%Y-%m-%d %H:%M:%S')
            mu_category_id = event.get("group").get("category", None)
            eb_category_id = 0

            event_deets = [event_name, event_url, event_img, source_event_id, description, start_time, eb_category_id, mu_category_id]
            event_details.append(event_deets)

        return event_details


                