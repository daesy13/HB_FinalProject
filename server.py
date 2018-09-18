"""Bar Ratings"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import Bar, BarPicture, Rating, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage2.html")
    # return "<html><body>Placeholder for the homepage.</body></html>"

@app.route('/bars')
def getbars():
    """Bar List Page"""
    eachBar=Bar.query.all()
    return render_template("bars.html", bars=eachBar)

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""
    user_id = request.form["user_id"]
    password = request.form["password"]

    # In an actual application, we'd check to see if this user was
    # in our database and if the password matched. For demo purposes,
    # we're assuming this is a valid user and logging them in.

    session["user_id"] = user_id

    return redirect("/bars")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
