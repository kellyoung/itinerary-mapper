"""Itinerary Mapper"""
import os

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify, url_for, send_from_directory)
from werkzeug import secure_filename

# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Trip, Place, Category, connect_to_db, db

import datetime

app = Flask(__name__)

app.secret_key = "PX78D1EBTcu3o4v8CK6i1EvtO7N6p3Ow"

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


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


@app.route('/<username>/trips')
def all_trips_page(username):
    in_session = session.get('username')

    if in_session == username:
        user = User.query.get(username)
        # user_trips = user.trips.order_by(Trip.start_date)
        user_trips = Trip.query.filter(Trip.username ==
                                       user.username).order_by(Trip.start_date).all()
        return render_template('all_trips.html',
                               user=user,
                               user_trips=user_trips)
    else:
        flash('You do not have access to this page.')
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

        # do this when have time to figure out encoding
        # trip_places_utf = []

        # for place in trip_places:
        #     print place.place_loc
        #     print type(place.place_loc)
        #     # print type(place.place_loc.encode('utf-8'))
        #     place_loc = unicode(place.place_loc)
        #     trip_places_utf.append((place, place_loc))

        # need to pass in all places too to be used in JINJA
        return render_template('trip_page.html',
                               user=user,
                               trip=trip,
                               trip_dates=trip_dates,
                               trip_places=trip_places)
    else:
        flash('You do not have access to this page.')
        return redirect('/')


@app.route('/create_trip.json', methods=['POST'])
def create_trip():
    """
    Adds trip information to database, then redirects to
    the trip's editing page.
    """
    username = session.get('username')
    trip_name = request.form.get('tripname')
    from_date = request.form.get('from')
    to_date = request.form.get('to')
    # latitude, longitude = request.form.get('coordinates').split(',')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    loc_name = request.form.get('loc-name')
    viewport = request.form.get('viewport')
    print viewport

    # DOESN't SEEM TO BE NECESSARY converts string dates to date objects
    # first_day = datetime.datetime.strptime(from_date, '%m/%d/%Y').date()
    # last_day = datetime.datetime.strptime(to_date, '%m/%d/%Y').date()

    # add info to trips table in database
    new_trip = Trip(trip_name=trip_name, start_date=from_date, end_date=to_date,
                    username=username, latitude=latitude, longitude=longitude,
                    viewport=viewport, general_loc=loc_name)

    db.session.add(new_trip)
    db.session.commit()

    # print trip_name, from_date, to_date, latitude, longitude, loc_name, viewport

    # return redirect('/create_trip/%s/%s' % (username, new_trip.trip_id))

    return jsonify({'status': 'success', 'username': new_trip.username,
                    'trip_id': new_trip.trip_id})


@app.route('/trip_loc_info.json')
def trip_loc_info():
    """
    JSON of the trip map info to be passed to the Add Place Map
    Needs the current trip_id's info
    """
    trip_id = int(request.args.get('trip_id'))
    trip = Trip.query.get(trip_id)

    print trip

    latitude = trip.latitude
    longitude = trip.longitude
    viewport = trip.viewport
    print latitude, longitude
    print viewport

    return jsonify({'latitude': latitude, 'longitude': longitude, 'viewport': viewport})


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

    # i need to add the picture in after creating new place so i can access
    # the place_id

    new_place = Place(place_name=place_name, place_loc=place_loc,
                      latitude=latitude, longitude=longitude, day_num=day_num,
                      date=date, trip_id=trip_id, cat_id=cat_id, notes=notes)

    db.session.add(new_place)
    db.session.commit()

    if 'pic' in request.files:
        print 'GET PICTURE HERE'
        pic_file = request.files['pic']
        if allowed_file(pic_file.filename):
            # I want to convert the filename
            extension = pic_file.filename.rsplit('.', 1)[1]
            filename = secure_filename('%s.%s' % (new_place.place_id, extension))
            pic_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #  add filename to database
            print filename
            new_place.pic_file = filename
    else:
        # go to the else and add a default pic into the database if nothing
        # need to find out what category it's in
        filename = cat_id + '.png'
        print filename
        new_place.pic_file = filename

    db.session.commit()
    img_url = url_for('uploaded_file', filename=new_place.pic_file)
    print img_url
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
                    <img src='%s' alt='%s picture'>
                    <button type="button" id="newly-added" class="btn btn-primary btn-sm edit-btn" data-toggle="modal" data-target="#editModal">
                      Edit Place
                    </button>
                    </div>
                    """ % (new_place.place_id, day_num, date, cat_id, place_name,
                           place_loc, notes, img_url, place_name)

    return jsonify({'place_id': new_place.place_id, 'new_place_div': new_place_div, 'place_loc': new_place.place_loc})


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


@app.route('/delete_trip.json', methods=['POST'])
def delete_trip():
    trip_id = int(request.form.get('trip_id'))

    trip_places = Place.query.filter(Place.trip_id == trip_id).all()
    trip = Trip.query.get(trip_id)

    print trip_places
    print trip

    # get the username to be passed
    username = trip.username
    # delete all places first
    for place in trip_places:
        db.session.delete(place)
    # then delete the trip itself
    db.session.delete(trip)

    db.session.commit()

    return jsonify({'status': 'success', 'username': username})


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
        place_loc = place.place_loc
        latitude = place.latitude
        longitude = place.longitude
        img_url = url_for('uploaded_file', filename=place.pic_file)
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
                    <img src='%s'>
                    </div>
                    """ % (place.place_id, day_num, place.date, category, title,
                           place.place_loc, place.notes, img_url)
        place_info = {'title': title, 'day_num': day_num, 'category': category,
                      'latitude': latitude, 'longitude': longitude, 'content': content,
                      'place_loc': place_loc}
        all_places[place.place_id] = place_info

    # jsonify it to be processed in front end
    return jsonify(all_places)


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    # DebugToolBarExtension(app)

    app.run(port=5000, host="0.0.0.0")
