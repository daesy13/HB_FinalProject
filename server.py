"""Bar Ratings"""
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Bar, BarPicture, User, Event, Rating, connect_to_db, db
from sqlalchemy import func

import secrets


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = secrets.FLASK_SECRET_KEY

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage2.html", road_name=None)
    # return "<html><body>Placeholder for the homepage.</body></html>"

# INVITATION PAGE PRIVATE USER
@app.route('/EVT')
def eventfb():
    """Private invitation with FB sharing."""
    if "user_id" in session:
        user_id = session["user_id"]
        eachBar = Bar.query.all()
        user = User.query.get(user_id)
        road_name = user.road_name
        event = Event.query.filter_by(user_id=user_id).all()

    return render_template("EVT3.html", bars=eachBar, road_name=road_name, event=event)
    # return "<html><body>Placeholder for the homepage.</body></html>"

# PUBLIC EVENT
@app.route('/PublicEvent')
def publicevent():
    """Homepage."""
    return render_template("publicevents.html")
    # return "<html><body>Placeholder for the homepage.</body></html>"

@app.route('/bars')
def getbars():
    """Bar List Page"""

    if "user_id" in session:
        user_id = session["user_id"]
        eachBar = Bar.query.all()
        user = User.query.get(user_id)
        ratings = Rating.query.filter_by(user_id=user_id).all()
        user_ratings = {}
        for rating in ratings:
            user_ratings[rating.bar_id] = rating.bar_rating

        bars = []
        for bar in eachBar:
            bar.user_rating = user_ratings.get(bar.bar_id)
            bars.append(bar)

        # bars1=db.session.query(Bar,Rating).outerjoin(Rating).filter_by(user_id=user_id).all()
        # bars2=db.session.query(Bar,Rating).outerjoin(Rating).filter_by(user_id= None).all()
        # bars=bars1+bars2
        # print(bars1)
        # print(bars2)

        # for bar in bars:
        #     print(bar)
        # select * from bars left join ratings using (bar_id) where user_id=1 or user_id IS NULL;

        road_name = user.road_name
        return render_template("Ubars.html", bars=bars, user_ratings=user_ratings, road_name=road_name)
    else:
        eachBar=Bar.query.all()

        # rating_avg = Rating.query.sum(bar_rating)/Rating.query.count(bar_rating)
        return render_template("barsfixpic.html", bars=eachBar, road_name=None)


@app.route('/bars', methods=['POST'])
def rate_bar():
    """Storing bar ratings"""

# Get form variables
    if "user_id" in session:
        user_id = session.get('user_id')
        stars = request.form.get('rating')
        bar_id = request.form.get('id')
        rating = Rating.query.filter_by(user_id=user_id, bar_id=bar_id).first()

        if not rating:
            # rating = Rating(bar_id=bar_id, user_id=user_id, bar_rating=stars)
            rating = Rating(bar_id=bar_id, user_id=user_id, bar_rating=None)
        else:
            rating.bar_rating = stars
            # # avg = Rating.query(func.avg(bar_rating).label('average')).scalar()
            # rating_avg = Rating.query.sum(bar_rating)/Rating.query.count(bar_rating)

        db.session.add(rating)
        db.session.commit()

    return ''

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""
    return render_template("/login.html", road_name=None)

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/register")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/profile")

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html", road_name=None)

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    name = request.form["name"]
    gender = request.form["gender"]
    road_name = request.form["road_name"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(user_name=name, gender=gender, road_name=road_name, email=email, password=password)

    user = User.query.filter_by(email=email).first()
    if user != None:
        flash("There is already an account with the same email address")
        return redirect("/login")

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added.")
    return redirect("/bars")
    # return redirect(f"/profile.html/{new_user.user_id}")

# PUBLIC Trip
@app.route("/trip", methods=["POST", "GET"] )
def events():
    """Map Page"""
    eachBar=Bar.query.all()

    """Event registration."""

    # Get form variables
    welcome = request.form.get("welcome")
    e_intro = request.form.get("short_intro")
    e_title = request.form.get("event_title")
    datepicker = request.form.get("datepicker")
    time = request.form.get("time")
    location = request.form.get("location")
    start = request.form.get("start")
    waypoints = request.form.get("waypoints")
    end = request.form.get("end")
    #********** if user_id "ON" public trips breaks and user session works fine
    # user_id = session["user_id"]

    if request.method == "POST":

        new_event = Event(welcome=welcome, e_intro=e_intro, e_title=e_title, e_date=datepicker, time=time, location_name=location, e_start=start, e_waypoints=waypoints, e_endpoint=end, user_id=user_id)


        db.session.add(new_event)
        db.session.commit()


    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        road_name = user.road_name
        # return render_template("PEvent.html", bars=eachBar, road_name=road_name)
        return render_template("PrivateE.html", bars=eachBar, road_name=road_name)


    else:
        return render_template("events.html", bars=eachBar, road_name=None)
    # create a function to able to use multiple times line 88-90 <----------
    # return render_template("events.html")
    # return "map's page"

def getbars():
    """Bar List Page"""
    eachBar=Bar.query.all()
    # return render_template("bars.html", bars=eachBar)

    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        road_name = user.road_name
        return render_template("PEvent.html", bars=eachBar, road_name=road_name)
    else:
        return render_template("bars.html", bars=eachBar, road_name=None)

# # PRIVATE TRIPS Maybe erase all these commented line if private trip doesn't work
# @app.route("/events")
# def events():
#     """Map Page"""
#     eachBar=Bar.query.all()

#     if "user_id" in session:
#         user_id = session["user_id"]
#         user = User.query.filter_by(user_id=user_id).first()
#         road_name = user.road_name
#         return render_template("events.html", bars=eachBar, road_name=road_name)
#     else:
#         return render_template("events.html", bars=eachBar, road_name=None)
#     # create a function to able to use multiple times line 88-90 <----------
#     # return render_template("events.html")
#     # return "map's page"

# def getbars():
#     """Bar List Page"""
#     eachBar=Bar.query.all()
#     # return render_template("bars.html", bars=eachBar)

#     if "user_id" in session:
#         user_id = session["user_id"]
#         user = User.query.filter_by(user_id=user_id).first()
#         road_name = user.road_name
#         return render_template("bars.html", bars=eachBar, road_name=road_name)
#     else:
#         return render_template("bars.html", bars=eachBar, road_name=None)

@app.route("/profile")
def profile():
    """Profile Page"""

    eachBar=Bar.query.all()

    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        road_name = user.road_name
        session["user_id"] = user.user_id
        return render_template("profile.html", road_name=road_name, user=user)
    else:
        return redirect("/register")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
