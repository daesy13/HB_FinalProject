"""Bar Ratings"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Bar, BarPicture, User, Rating, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage2.html", road_name=None)
    # return "<html><body>Placeholder for the homepage.</body></html>"

@app.route('/bars')
def getbars():
    """Bar List Page"""
    eachBar=Bar.query.all()

    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        road_name = user.road_name
        return render_template("bars.html", bars=eachBar, road_name=road_name)
    else:
        return render_template("bars.html", bars=eachBar, road_name=None)

# def rate_bar():<---create new function for ratings
# @app.route('/bars', methods=['POST'])
# def rate_bar():




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

@app.route("/events")
def events():
    """Map Page"""
    eachBar=Bar.query.all()

    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        road_name = user.road_name
        return render_template("events.html", bars=eachBar, road_name=road_name)
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
        return render_template("bars.html", bars=eachBar, road_name=road_name)
    else:
        return render_template("bars.html", bars=eachBar, road_name=None)

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
