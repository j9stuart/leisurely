# Functions to be used for server file

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
from model import connect_to_db, db, Category, Weekday, WeekdayCategory, Activity, User, SavedEvent
import meetup.api
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
from bcrypt import hashpw, gensalt
import geocoder
import re

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


MEETUP_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/8/80/Meetup_square.png"
EVBRTE_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/8/87/Eventbrite_wordmark_orange.jpg"



def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
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





                