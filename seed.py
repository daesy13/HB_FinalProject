"""Utility file to seed ratings database from Bar & User data in seed_data/"""

import datetime

from sqlalchemy import func
from model import User
from model import Bar
from model import Rating
from model import Event

from model import connect_to_db, db
from server import app


def load_users(users_file):
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for i, row in enumerate(open(users_file)):
        row = row.rstrip()
        print(row)
        user_id, user_name, email, password, gender, road_name, somethingabout, image_file = row.split("|")

        users = User(user_id=user_id,
                    user_name=user_name,
                    email=email,
                    password=password,
                    road_name=road_name,
                    gender=gender,
                    somethingabout=somethingabout,
                    image_file=image_file)

        # We need to add to the session or it won't ever be stored
        db.session.add(users)

        # provide some sense of progress
        # if i % 100 == 0:
        #     print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_bars(bars_file):
    """Load users from u.user into database."""

    print("Bars")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Bar.query.delete()

    # Read u.user file and insert data
    for i, row in enumerate(open(bars_file)):
        row = row.rstrip()
        print(row)
        bar_id, bar_name, bar_address, bar_city, bar_state, bar_zip, bar_phone, bar_pic = row.split("|")

        bars = Bar(bar_id=bar_id,
                    bar_name=bar_name,
                    bar_address=bar_address,
                    bar_city=bar_city,
                    bar_state=bar_state,
                    bar_zip=bar_zip,
                    bar_phone=bar_phone,
                    bar_pic=bar_pic)

        # We need to add to the session or it won't ever be stored
        db.session.add(bars)

        # provide some sense of progress
        # if i % 100 == 0:
        #     print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_ratings(ratings_file):
    """Load users from u.user into database."""

    print("Ratings")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

    # Read u.user file and insert data
    for i, row in enumerate(open(ratings_file)):
        row = row.rstrip()
        print(row)
        rating_id, bar_id, user_id, bar_rating = row.split("|")

        ratings = Rating(rating_id=rating_id,
                    bar_id=bar_id,
                    user_id=user_id,
                    bar_rating=bar_rating)

        # We need to add to the session or it won't ever be stored
        db.session.add(ratings)

        # provide some sense of progress
        # if i % 100 == 0:
        #     print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_events(events_file):
    """Load events from u.user into database."""

    print("Events")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate events
    Event.query.delete()

    # Read u.user file and insert data
    for i, row in enumerate(open(events_file)):
        row = row.rstrip()
        print(row)
        e_id, user_id, welcome, e_intro, e_title, e_date, time, location_name, e_start, e_waypoints, e_endpoint = row.split("|")

        events = Event(e_id=e_id,
                    user_id=user_id,
                    welcome=welcome,
                    e_intro=e_intro,
                    e_title=e_title,
                    e_date=e_date,
                    time=time,
                    location_name=location_name,
                    e_start=e_start,
                    e_waypoints=e_waypoints,
                    e_endpoint=e_endpoint)

        # We need to add to the session or it won't ever be stored
        db.session.add(events)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    users_file = "seed_data/u.data"
    bars_file = "seed_data/b.info"
    ratings_file = "seed_data/r.rating"
    events_file = "seed_data/e.info"
    load_users(users_file)
    load_bars(bars_file)
    load_ratings(ratings_file)
    load_events(events_file)
    set_val_user_id()


