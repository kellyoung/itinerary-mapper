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
    trip_name = request.form.get('tripname')
    from_date = request.form.get('from')
    to_date = request.form.get('to')
    latitude, longitude = request.form.get('coordinates').split(',')
    loc_name = request.form.get('loc-name')

    # DOESN't SEEM TO BE NECESSARY converts string dates to date objects
    # first_day = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
    # last_day = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()

    #add info to trips table in database
    new_trip = Trip(trip_name=trip_name, start_date=from_date, end_date=to_date,
                    username=username, latitude=latitude, longitude=longitude,
                    general_loc=loc_name)

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
                    <button type="button" id="newly-added" class="btn btn-primary btn-sm edit-btn" data-toggle="modal" data-target="#editModal">
                      Edit Place
                    </button>
                    </div>
                    """ % (new_place.place_id, day_num, date, cat_id, place_name,
                           place_loc, notes)

    return jsonify({'place_id': new_place.place_id, 'new_place_div': new_place_div})


@app.route('/edit_place_info.json')
def get_place_info():
    """
    Passes back info to Edit place Form
    """

    place_id = request.args.get('place_id')
    select_place = Place.query.get(place_id)
    formatted_date = select_place.date.strftime("%Y-%m-%d")

    return jsonify({'place_id': place_id, 'place_name': select_place.place_name,
                    'place_loc': select_place.place_loc, 'latitude': select_place.latitude,
                    'longitude': select_place.longitude, 'day_num': select_place.day_num,
                    'trip_id': select_place.trip_id,
                    'cat_id': select_place.cat_id, 'notes': select_place.notes,
                    'formatted_date': formatted_date})


@app.route('/delete_place.json', methods=['POST'])
def delete_place():
    """
    Deletes a place by trip_id submitted and rerenders the create trip page.
    """

    place_id = request.form.get('place_id')

    place_to_delete = Place.query.get(int(place_id))

    db.session.delete(place_to_delete)
    db.session.commit()
    #  destination = url_for('.create_trip', username=username, trip_id=trip_id)

    return jsonify({'status': 'Deleted'})


@app.route('/edit_place.json', methods=['POST'])
def edit_place():
    place_id = request.form.get('place_id')
    place_name = request.form.get('place_name')
    place_search = request.form.get('place_search')
    visit_day = request.form.get('visit_day')
    day_num, date = visit_day.split(',')
    category = request.form.get('category')
    notes = request.form.get('notes')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    place_to_edit = Place.query.get(int(place_id))

    if place_name != place_to_edit.place_name:
        place_to_edit.place_name = place_name

    if place_search != place_to_edit.place_loc:
        place_to_edit.place_loc = place_search

    if int(day_num) != place_to_edit.day_num:
        place_to_edit.day_num = int(day_num)

    if date != place_to_edit.date.strftime("%Y-%m-%d"):
        place_to_edit.date = date

    if category != place_to_edit.cat_id:
        place_to_edit.cat_id = category

    if notes != place_to_edit.notes:
        place_to_edit.notes = notes

    if latitude and longitude:
        place_to_edit.latitude = latitude
        place_to_edit.longitude = longitude

    db.session.commit()

    return jsonify({'status': 'Edited'})


@app.route('/<username>/<trip_id>/mapview')
def display_map(username, trip_id):
    """
    Show a page of the trip as a map view. Has logic in
    render template to render differently based on whether
    if user is logged in, trip is published, and if trip is
    private.
    """
    user = User.query.get(username)
    trip = Trip.query.get(trip_id)
    username = session.get('username')

    if username or trip.published:
        return render_template('map_view.html',
                               user=user,
                               trip=trip,
                               username=username)
    else:
        flash('Sorry! You don\'t have access to this page.')
        return redirect('/')


@app.route('/publish_trip.json', methods=['POST'])
def publish_trip():
    trip_id = request.form.get('trip_id')
    target_trip = Trip.query.get(int(trip_id))

    if target_trip.published:
        target_trip.published = False
    else:
        target_trip.published = True

    print target_trip.published
    db.session.commit()

    return jsonify({'status': target_trip.published})


@app.route('/places_to_map.json')
def return_all_places():
    """passes back info of all places in trip as json"""
    # get trip by id and find all its places
    trip_id = request.args.get('trip_id')
    places = Trip.query.get(int(trip_id)).places

    # the info to be passed back to front end
    all_places = {}

    # get info for each place and add it to the all_places dictionary
    for place in places:
        title = place.place_name
        day_num = place.day_num
        category = place.cat_id
        latitude = place.latitude
        longitude = place.longitude
        content = """
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
                    </div>
                    """ % (place.place_id, day_num, place.date, category, title,
                           place.place_loc, place.notes)
        place_info = {'title': title, 'day_num': day_num, 'category': category,
                      'latitude': latitude, 'longitude': longitude, 'content': content}
        all_places[place.place_id] = place_info

    # jsonify it to be processed in front end
    return jsonify(all_places)


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    # DebugToolBarExtension(app)

    app.run(port=5000, host="0.0.0.0")
