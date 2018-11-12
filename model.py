"""Models and database for NOMADS project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this throught the Flask-SQLAlchemy helper library. On this, we can
# find the 'session' object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()

# Model definition

class User(db.Model):
    """User of Nomads website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(100), unique=True, nullable=True)
    #check and use enum type
    gender = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=True)
    password = db.Column(db.String(64), nullable=True)
    road_name = db.Column(db.String(15), nullable=True)
    somethingabout = db.Column(db.String(512), nullable=True, default='I love riding')
    image_file = db.Column(db.String(512), nullable=True, default='/static/default.png')


    def __repr__(self):
        return f"<User user_id={self.user_id} user_name={self.user_name} road_name={self.road_name}>"

# class UserPic

class Bar(db.Model):
    """List of bars and grill"""

    __tablename__ = "bars"

    bar_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bar_name = db.Column(db.String(255), nullable=False)
    bar_address = db.Column(db.String(255), nullable=False)
    bar_city = db.Column(db.String(100), nullable=False)
    bar_state = db.Column(db.String(100), nullable=False)
    bar_zip = db.Column(db.Integer, nullable=False)
    bar_phone = db.Column(db.String(15), nullable=True)
    bar_pic = db.Column(db.String(512), nullable=True)
    # bar_pic = db.Column(db.String(512), nullable=True, default='/static/bardefault.jpg')
    # bar_avg = db.Column(db.Integer, default=0)
    # there is another way gor actual pics

    def __repr__(self):
        return f"<Bar bar_id={self.bar_id} bar_name={self.bar_name} bar_city={self.bar_city}>"


class BarPicture(db.Model):
    """Picture of the bar"""

    __tablename__ = "barpictures"

    picture_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_picture = db.Column(db.String(200), nullable=False)
    bar_id = db.Column(db.Integer, db.ForeignKey('bars.bar_id'), nullable=False)

    # Define relationship to barsandgrill
    bar = db.relationship("Bar", backref=db.backref("barpictures", order_by=picture_id))

    def __repr__(self):
        return f"<BarPicture picture_id={self.picture_id} bar_name={self.bar.bar_name}>"


class Rating(db.Model):
    """Rating of bar by a user"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bar_id = db.Column(db.Integer, db.ForeignKey('bars.bar_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    bar_rating = db.Column(db.Integer, nullable=True)

    # Define relationship to bars
    bar = db.relationship("Bar", backref=db.backref("ratings", order_by=rating_id))

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} bar_id={self.bar_id} bar_rating={self.bar_rating}>"

class Event(db.Model):
    """Save data for user's events"""

    __tablename__ = "events"

    e_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    welcome=db.Column(db.String(255), nullable=True)
    e_intro=db.Column(db.String(255), nullable=True)
    e_title=db.Column(db.String(255), nullable=False)
    e_date=db.Column(db.String(10), nullable=True)
    time=db.Column(db.String(10), nullable=False)
    location_name=db.Column(db.String(255), nullable=False)
    e_start=db.Column(db.String(255), nullable=False)
    e_waypoints=db.Column(db.String(1000), nullable=False)
    e_endpoint=db.Column(db.String(255), nullable=False)

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("events", order_by=user_id))

    def __repr__(self):
        return f"<Rating e_id={self.e_id} e_title={self.e_title} e_date={self.e_date}>"

def connect_to_db(app):
    """Connect the database to our Flask app"""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///barratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")




