from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################

class Category(db.Model):
    """Categories from Eventbrite API"""

    __tablename__ = "categories"   

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    screenname = db.Column(db.String(80), nullable=False)

    weekdays = db.relationship("Weekday",
                                secondary="weekday_categories",
                                backref="categories")

    def __repr__(self):
        """Prints object in user-friendly format"""

        return "<Category: {}>".format(self.name)


class Weekday(db.Model):
    """Days of the Week"""

    __tablename__ = "weekdays"

    weekday_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class WeekdayCategory(db.Model):
    """Assocation table for weekdays and categories"""

    __tablename__ = "weekday_categories"

    weekday_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cat_id = db.Column(db.Integer, 
                       db.ForeignKey("categories.cat_id"),
                       nullable=False)
    weekday_id = db.Column(db.Integer, 
                       db.ForeignKey("weekdays.weekday_id"),
                       nullable=False)
    

class Activity(db.Model):
    """List of activities to be mapped to categories"""

    __tablename__ = "activities"

    act_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cat_id = db.Column(db.Integer,
                       db.ForeignKey('categories.cat_id'),
                       nullable=False)
    eb_cat_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    act_type = db.Column(db.String(80), nullable=True)
    eb_format_id = db.Column(db.Integer, nullable=False)
    sub_cat = db.Column(db.String(80), nullable=True)
    mu_id = db.Column(db.Integer, nullable=False)
    
    category = db.relationship('Category', backref='activities')


    def __repr__(self):
        """Prints object in user-friendly format"""

        return "<Activity: {}>".format(self.name)

class User(db.Model):
    """List of users who have created accounts"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class SavedEvent(db.Model):
    """List of saved events to be mapped to users"""

    __tablename__ = "saved_events"

    saved_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.BigInteger, nullable=False)
    event_name = db.Column(db.String(200), nullable=False)
    event_url = db.Column(db.String(200), nullable=False)

    user = db.relationship('User', backref=db.backref('saved_events', order_by=saved_id))






###############################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure the PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///leisurely'
    db.app = app
    db.init_app(app)

if __name__=="__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."