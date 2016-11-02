from sqlalchemy import func
from model import Category
from model import Weekday
from model import WeekdayCategory
from model import Activity
from datetime import datetime
import re

from model import connect_to_db, db
from server import app



def load_categories():
    """Load users from categories.csv into database"""

    print "Categories"

    # Delete all rows in table, so if we need to run this a second time, 
    # we won't be adding duplicate categories
    Category.query.delete()

    # Read category.csv file and insert data
    for row in open("seed_data/categories.csv"):
        row = row.rstrip()
        cat_id, name, screenname = row.split(",")

        category = Category(cat_id=cat_id,
                            name=name,
                            screenname=screenname)

        # Need to add to session to store 
        db.session.add(category)

    # Commit my work

    db.session.commit()


def load_weekdays():
    """Load weekdays from weekday.csv"""

    print "Weekdays"

    # Delete all rows in table, so if we need to run this a second time, 
    # we won't be adding duplicate categories
    Weekday.query.delete()

    # Read category.csv file and insert data
    for row in open("seed_data/weekday.csv"):
        row = row.rstrip()
        weekday_id, name = row.split(",")

        weekday = Weekday(weekday_id=weekday_id,
                            name=name,)

        # Need to add to session to store 
        db.session.add(category)

    # Commit my work

    db.session.commit()


def load_weekdaycategory():
    """Load weekdaycategories from weekdaycategory.csv"""

    print "Weekday_Categories"

    # Delete all rows in table, so if we need to run this a second time, 
    # we won't be adding duplicate categories
    WeekdayCategory.query.delete()

    # Read category.csv file and insert data
    for row in open("seed_data/weekdaycategory.csv"):
        row = row.rstrip()
        weekday_category_id, name = row.split(",")

        weekday_category = WeekdayCategory(weekday_category_id=weekday_category_id, 
                                           name=name,)

        # Need to add to session to store 
        db.session.add(category)

    # Commit my work

    db.session.commit()


def load_activities():
    """Load activities from activities.csv into database"""

    print "Activities"

    # Delete all rows in table, so if we need to run this a second time, 
    # we won't be adding duplicate categories
    Activity.query.delete()

    # Read category.csv file and insert data
    for row in open("seed_data/activities.csv"):
        row = row.rstrip()
        act_id, cat_id, name, act_type, sub_cat = row.split(",")

        category = Category(act_id=act_id, 
                            cat_id=cat_id,
                            name=name,
                            act_type=act_type,
                            sub_cat=sub_cat)

        # Need to add to session to store 
        db.session.add(category)

    # Commit my work

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_categories()
    load_weekdays()
    load_weekdaycategory()
    load_activities()