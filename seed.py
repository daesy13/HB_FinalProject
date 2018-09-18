"""Utility file to seed ratings database from Bar & User data in seed_data/"""

import datetime

from sqlalchemy import func
from model import User
from model import Bar

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
        user_id, user_name, email, password, gender, road_name = row.split("|")

        users = User(user_id=user_id,
                    user_name=user_name,
                    email=email,
                    password=password,
                    road_name=road_name,
                    gender=gender)

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
        bar_id, bar_name, bar_address, bar_city, bar_state, bar_zip, bar_phone = row.split("|")

        bars = Bar(bar_id=bar_id,
                    bar_name=bar_name,
                    bar_address=bar_address,
                    bar_city=bar_city,
                    bar_state=bar_state,
                    bar_zip=bar_zip,
                    bar_phone=bar_phone)

        # We need to add to the session or it won't ever be stored
        db.session.add(bars)

        # provide some sense of progress
        # if i % 100 == 0:
        #     print(i)

    # Once we're done, we should commit our work
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    users_file = "seed_data/u.data"
    bars_file = "seed_data/b.info"
    load_users(users_file)
    load_bars(bars_file)


