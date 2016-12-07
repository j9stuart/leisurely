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
        cat_id, name, screenname, img_url = row.split(",")

        category = Category(cat_id=cat_id,
                            name=name,
                            screenname=screenname,
                            img_url=img_url)

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
        db.session.add(weekday)

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
        weekday_category_id, cat_id, weekday_id = row.split(",")

        weekday_category = WeekdayCategory(weekday_category_id=weekday_category_id, 
                                           cat_id=cat_id,
                                           weekday_id=weekday_id)

        # Need to add to session to store 
        db.session.add(weekday_category)

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
        act_id, cat_id, eb_cat_id, name, act_type, eb_format_id, sub_cat, mu_id, img_url = row.split(",")

        activity = Activity(act_id=act_id, 
                            cat_id=cat_id,
                            eb_cat_id=eb_cat_id,
                            name=name,
                            act_type=act_type,
                            eb_format_id=eb_format_id,
                            sub_cat=sub_cat,
                            mu_id=mu_id,
                            img_url=img_url)

        # Need to add to session to store 
        db.session.add(activity)

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
