"""Itinerary Mapper"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Trip, Place, Category, connect_to_db, db

import datetime

app = Flask(__name__)

app.secret_key = "PX78D1EBTcu3o4v8CK6i1EvtO7N6p3Ow"

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """
    Show homepage. Has login, logout, signup, create trip,
    and go to trip. Displays depending on if username is
    in session and if user has a trip or not.
    """

    # check to see if user is logged in
    username = session.get('username')

    # check to see if the user has a trip or not
    user_trip = Trip.query.filter(Trip.username == username).first()

    return render_template('homepage.html',
                           username=username,
                           user_trip=user_trip)


@app.route('/login', methods=['POST'])
def login():
    """Checks login info, adds to session if successful, redirects to home."""

    # get arguments from login
    username = request.form.get('username')
    password = request.form.get('password')

    # check to see if username is valid and in database
    check_username = db.session.query(User).filter(User.username ==
                                                   username).first()

    if not username or not password:
        flash('Please enter a username and password.')
    elif check_username and check_username.password == password:
        session['username'] = check_username.username
        flash('Welcome, %s!' % check_username.name)
    elif check_username:
        flash('Incorrect Password. Please try again.')
    else:
        flash('The username and password do not exist. Try again.')

    return redirect('/')


@app.route('/logout')
def logout():
    """Remove username from session and return to homepage"""

    username = session.pop('username')
    flash('Logged out of %s.' % username)

    return redirect('/')


@app.route('/create_user', methods=['POST'])
def create_user():
    """
    If form inputs valid, creates a user and adds to the database.
    Returns to homepage and asks user to login.
    """
    # get form inputs
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    # see if user already exists
    check_users_existance = User.query.filter(User.username == username).first()

    # if username is already in the database
    if check_users_existance:
        flash('%s is already taken. Please try again.' % username)
    # if username isn't taken, add to the database.
    else:
        new_user = User(name=name, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('The account %s was successfully created. Please log in.' %
              username)
    return redirect('/')


@app.route('/create_trip/<username>/<trip_id>')
def trip_page(username, trip_id):
    in_session = session.get('username')

    if in_session == username:
        user = User.query.get(username)
        trip = Trip.query.get(trip_id)

        trip_dates = []

        delta = trip.end_date - trip.start_date

        for index, i in enumerate(range(delta.days + 1)):
            trip_date = trip.start_date + datetime.timedelta(days=i)
            trip_date_str = trip_date.strftime("%B %d, %Y")
            trip_dates.append((index+1, trip_date, trip_date_str))

        trip_places = Place.query.filter(Place.trip_id == trip_id).all()
        # need to pass in all places too to be used in JINJA
        return render_template('trip_page.html',
                               user=user,
                               trip=trip,
                               trip_dates=trip_dates,
                               trip_places=trip_places)
    else:
        flash('You do not have access to this page.')
        return redirect('/')


@app.route('/create_trip', methods=['POST'])
def create_trip():
    """
    Adds trip information to database, then redirects to
    the trip's editing page.
    """
    username = session.get('username')
    print username
    trip_name = request.form.get('tripname')
    from_date = request.form.get('from')
    to_date = request.form.get('to')

    # DOESN't SEEM TO BE NECESSARY converts string dates to date objects
    # first_day = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
    # last_day = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()

    #add info to trips table in database
    new_trip = Trip(trip_name=trip_name, start_date=from_date, end_date=to_date,
                    username=username)

    db.session.add(new_trip)
    db.session.commit()

    print new_trip.trip_id

    return redirect('/create_trip/%s/%s' % (username, new_trip.trip_id))


@app.route('/add_place.json', methods=['POST'])
def add_place():
    """
    Takes info from front end and adds to trips database, returns a json
    with information to be added to the front end.
    """

    place_name = request.form.get('placename')
    place_loc = request.form.get('placesearch')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    day_num = int(request.form.get('daynum'))
    date = request.form.get('visitday')
    trip_id = int(request.form.get('trip_id'))
    cat_id = request.form.get('category')
    notes = request.form.get('notes')

    new_place = Place(place_name=place_name, place_loc=place_loc,
                      latitude=latitude, longitude=longitude, day_num=day_num,
                      date=date, trip_id=trip_id, cat_id=cat_id, notes=notes)

    db.session.add(new_place)
    db.session.commit()

    new_place_div = """
                    <div id='place-div-%s' class='place-div'>
                    <h5>Day:</h5>
                    <p>Day %s: %s</p>
                    <h5>Category:</h5>
                    <p>%s</p>
                    <h5>Place Name:</h5>
                    <p>%s</p>
                    <h5>Place Address:</h5>
                    <p>%s</p>
                    <h5>Notes:</h5>
                    <p>%s</p>
                    <button type="button" class="btn btn-primary btn-sm edit-btn" data-toggle="modal" data-target="#editModal">
                      Edit Place
                    </button>
                    </div>
                    """ % (new_place.place_id, day_num, date, cat_id, place_name,
                           place_loc, notes)

    return jsonify({'place_id': new_place.place_id, 'new_place_div': new_place_div})


@app.route('/edit_place_info.json')
def get_place_info():
    place_id = request.args.get('place_id')
    select_place = Place.query.get(place_id)
    formatted_date = select_place.date.strftime("%Y-%m-%d")

    return jsonify({'place_id': place_id, 'place_name': select_place.place_name,
                    'place_loc': select_place.place_loc, 'latitude': select_place.latitude,
                    'longitude': select_place.longitude, 'day_num': select_place.day_num,
                    'date': select_place.date, 'trip_id': select_place.trip_id,
                    'cat_id': select_place.cat_id, 'notes': select_place.notes,
                    'formatted_date': formatted_date})

if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    # DebugToolBarExtension(app)

    app.run(port=5000, host="0.0.0.0")
