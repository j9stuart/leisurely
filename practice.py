class Event(db.Model):
    """List of all events"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_name = db.Column(db.String(200), nullable=False)
    event_url = db.Column(db.String(200), nullable=False)
    event_img = db.Column(db.String(200), nullable=False)
    source_event_id = db.Column(db.BigInteger, nullable=False)
    description = db.Column(db.String(3000), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    eb_category_id = db.Column(db.Integer, nullable=False)
    mu_category_id = db.Column(db.Integer, nullable=False)


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

    event_details2 = seed_events("meetup")

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



def seed_events(source):
    """ Creates table for all eventbrite and meetup events """
    event_details = []
    i = 1

    if source == "eventbrite":
        while i <= 50:
            source = 1
            events = eventbrite.get("/events/search/?location.address=san%20francisco&page="+str(i))
            event_list = events.get("events")
            for event in event_list:
                event_name = event.get("name").get("text")
                event_url = event.get("url")
                event_img = event.get("logo", EVBRTE_IMG_URL).get("original", {"photo_link": EVBRTE_IMG_URL}).get("url", EVBRTE_IMG_URL)
                source_event_id = event.get("id")
                description = event.get("description").get("text")
                uc_time = event.get("start").get("utc")
                time = datetime.datetime.strptime(uc_time, '%Y-%m-%dT%H:%M:%SZ')
                start_time = time.strftime('%Y-%m-%d %H:%M:%S')
                eb_category_id = event.get("category_id")
                mu_category_id = 0

                event_deets = [event_name, event_url, event_img, source_event_id, description, start_time, eb_category_id, mu_category_id]
                event_details.append(event_deets)
                i += 1

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

