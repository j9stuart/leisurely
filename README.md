# Leisurely

Leisurely is an event discovery application that provides users with a list of events and activities based on their choice of location, category, time frame, and price. Users can filter for events happening today, this week, or this month. Users can also filter for free or paid events.  

<a href="http://imgur.com/m6lJofh"><img src="http://i.imgur.com/m6lJofh.png" title="source: imgur.com" /></a>

## Table of Contents

* [Tech Stack](#tech-stack)
* [Feature Demo](#demo)
* [Set-up & Installation](#setup)
* [Next Steps](#todo)

## <a name="tech-stack"></a>Tech Stack:

__Frontend:__ HTML5, Javascript, jQuery, Bootstrap, AJAX <br/>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy, bcrypt <br/>
__APIs:__ Eventbrite, Meetup, Google Maps <br/>

## <a name="demo"></a>Feature Demo 

<a href="http://imgur.com/vD8IceA"><img src="http://i.imgur.com/vD8IceA.gif" title="source: imgur.com" /></a>

## <a name="setup"></a>Set-up & Installation:

- Python 2.7
- Installation of PostgreSQL
- Eventbrite, Meetup, and Google Maps API keys

To run this application on your local server, follow the steps below:

Clone repository:
```
$ git clone https://github.com/j9stuart/leisurely.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install requirements:
```
$ pip install -r requirements.txt
```
You will need your own secret key for <a href="http://www.eventbrite.com/developer/v3/quickstart/" target="_blank">Eventbrite</a>, <a href="https://secure.meetup.com/meetup_api/key/" target="_blank">Meetup</a> and <a href="https://developers.google.com/maps/documentation/javascript/get-api-key" target="_blank">Google Maps</a>. Save them to a file `secrets.sh`.  

Create database 'leisurely':
```
$ createdb leisurely
```
Create your database tables:
```
$ python -i model.py
db.create_all()
```
Seed your category and activity tables:
```
$ python seed.py
```
Run the app from the command line:
```
$ python server.py
```

## <a name="todo"></a>Next Steps:
* Implement caching to reduce latency
* Allow more dynamic searching using whoosh or elastic search
* Add Facebook Oauth to integrate and leverage Facebook data
* Use web scraping to improve results and enhance event discovery for users
