"""Itinerary Mapper"""
import os

import bcrypt

import facebook

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify, url_for, send_from_directory)
from flask_oauth import OAuth

from werkzeug import secure_filename

# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Trip, Place, Category, connect_to_db, db

import datetime

app = Flask(__name__)

oauth = OAuth()



app.secret_key = "PX78D1EBTcu3o4v8CK6i1EvtO7N6p3Ow"

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'JPG', 'PNG'])

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET = os.environ['FACEBOOK_APP_SECRET']

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('age_range, gender, name, picture, id')}
)
# --------------------------------------------------------------------------- #
@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@app.route("/facebook_logout")
def facebook_logout():
    pop_login_session()
    return redirect(url_for('index'))

def allowed_file(filename):
    """check if file is a valid name
    >>> allowed_file('dog.png')
    True

    >>> allowed_file('dog.gif')
    False
    """
    print '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """a route to where files are stored to access pictures"""
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

    return render_template('homepage.html',
                           username=username)


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

    if not check_username:
        flash('The username and password do not exist. Try again.')
    elif bcrypt.hashpw(str(password), str(check_username.password)) == str(check_username.password):
        session['username'] = check_username.username
        flash('Welcome, %s!' % check_username.name)
    elif check_username:
        flash('Incorrect Password. Please try again.')

    return redirect('/')


# @app.route('/fb_login.json', methods=['POST'])
# def fb_login():
#     """Checks to see if user has logged in before, if not, store info in DB"""
#     token = request.form.get('token')
#     user_id = request.form.get('user_id')

#     graph = facebook.GraphAPI(token)
#     args = {'fields': 'name'}
#     profile = graph.get_object('me', **args)
#     print profile

#     check_username = db.session.query(User).filter(User.username ==
#                                                    user_id).first()
#     session['username'] = profile['id']
#     print session['username']
#     if not check_username:
#         # will need to fix password part, password should be an opt. parameter
#         # this will prevent people from trying to manually enter into FB accounts
#         # and won't have to store sensitive data
#         new_user = User(name=profile['name'], username=user_id, password='fb_user')
#         db.session.add(new_user)
#         db.session.commit()
#     # flash('Welcome, %s!') % profile['name']
#     return jsonify({'status': 'logged in'})


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
    hashed_pw = bcrypt.hashpw(str(password), bcrypt.gensalt())

    if bcrypt.hashpw(str(password), hashed_pw) == hashed_pw:
        print "It matches"

    # see if user already exists
    check_users_existance = User.query.filter(User.username == username).first()

    # if username is already in the database
    if check_users_existance:
        flash('%s is already taken. Please try again.' % username)
    # if username isn't taken, add to the database.
    else:
        new_user = User(name=name, username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username
        flash('The account %s was successfully created. You are now signed in.' %
              username)
    return redirect('/')


@app.route('/<username>/trips')
def all_trips_page(username):
    in_session = session.get('username')
    print 'in username/trips'
    print in_session
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


def create_date_range(start, end):
    """
    takes a start date object and an end date object
    and generates the dates between and returns all
    of the dates as a list. It's a list of tuple that
    gives day number, trip_date object, and trip_date
    as a string.

    >>> create_date_range(datetime.date(2010, 5, 24), datetime.date(2010, 5, 25)) # doctest: +NORMALIZE_WHITESPACE
    [(1, datetime.date(2010, 5, 24), 'May 24, 2010'),
    (2, datetime.date(2010, 5, 25), 'May 25, 2010')]
    """
    trip_dates = []

    delta = end - start

    for index, i in enumerate(range(delta.days + 1)):
            trip_date = start + datetime.timedelta(days=i)
            trip_date_str = trip_date.strftime("%B %d, %Y")
            trip_dates.append((index+1, trip_date, trip_date_str))

    return trip_dates


@app.route('/create_trip/<username>/<trip_id>')
def trip_page(username, trip_id):
    """
    Takes information from trip creation form
    and renders the template with the information.
    """
    in_session = session.get('username')

    if in_session == username:
        user = User.query.get(username)
        trip = Trip.query.get(int(trip_id))

        # create dates between start date and end date
        trip_dates = create_date_range(trip.start_date, trip.end_date)

        trip_places = Place.query.filter(Place.trip_id == trip_id).all()

        trip_places_utf = []
        for place in trip_places:
            # needs to be encoded in case google places address is non-latin
            place_loc = place.place_loc.encode('utf-8')
            trip_places_utf.append((place, place_loc))

        # need to pass in all places too to be used in JINJA
        return render_template('trip_page.html',
                               user=user,
                               trip=trip,
                               trip_dates=trip_dates,
                               trip_places=trip_places_utf)
    else:
        # handle if someone is trying to access the route directly without
        # signing in
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
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    loc_name = request.form.get('loc-name')
    viewport = request.form.get('viewport')

    # add info to trips table in database
    new_trip = Trip(trip_name=trip_name, start_date=from_date, end_date=to_date,
                    username=username, latitude=latitude, longitude=longitude,
                    viewport=viewport, general_loc=loc_name)

    db.session.add(new_trip)
    db.session.commit()

    return jsonify({'status': 'success',
                    'username': new_trip.username,
                    'trip_id': new_trip.trip_id})


@app.route('/trip_loc_info.json')
def trip_loc_info():
    """
    JSON of the trip map info to be passed to the Add Place Map
    Needs the current trip_id's info
    """
    trip_id = int(request.args.get('trip_id'))
    trip = Trip.query.get(trip_id)

    latitude = trip.latitude
    longitude = trip.longitude
    viewport = trip.viewport

    return jsonify({'latitude': latitude,
                    'longitude': longitude,
                    'viewport': viewport})


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

    # handle pictures
    if 'pic' in request.files:
        print 'GET PICTURE HERE'
        pic_file = request.files['pic']
        if allowed_file(pic_file.filename):
            # convert the filename to the place_id its associated with
            extension = pic_file.filename.rsplit('.', 1)[1]
            filename = secure_filename('%s.%s' % (new_place.place_id,
                                                  extension))
            pic_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #  add filename to database
            new_place.pic_file = filename
    else:
        # go to the else and add a default pic into the database if nothing
        # need to find out what category it's in
        filename = cat_id + '.png'
        new_place.pic_file = filename

    db.session.commit()
    img_url = url_for('uploaded_file', filename=new_place.pic_file)

    # div that will be added dynamically to page for new place added
    if cat_id == 'eat':
        icon = 'cutlery'
    elif cat_id == 'sleep':
        icon = 'bed'
    elif cat_id == 'explore':
        icon = 'globe'
    elif cat_id == 'transport':
        icon = 'paper-plane'

    new_place_div_test = """
                    <div id='place-div-%s'class='col-lg-3 col-md-4 col-xs-6 place-div'>
                        <div class='place-content'>

                        <div class='place-img-div'>
                            <img src='%s' alt='%s picture' class='place-img'>
                        </div>

                        <div class='place-text'>
                            <p class='place-text-name text-%s'>
                                %s
                                <i class="fa fa-%s"></i>
                            <p class='utf-8 place-address'>%s</p>
                        </div>
                        <button type="button" id="newly-added" class="edit-btn"
                        data-toggle="modal" data-target="#editModal">
                          Edit Place
                        </button>
                        </div>
                    </div>
                    """ % (new_place.place_id, img_url, place_name,
                           cat_id, place_name, icon, place_loc)

    return jsonify({'place_id': new_place.place_id,
                    'new_place_div': new_place_div_test,
                    'place_loc': new_place.place_loc})


@app.route('/edit_place_info.json')
def get_place_info():
    """
    Passes back info to Edit Place Form to display it
    """

    place_id = request.args.get('place_id')
    select_place = Place.query.get(place_id)
    formatted_date = select_place.date.strftime("%Y-%m-%d")

    return jsonify({'place_id': place_id,
                    'place_name': select_place.place_name,
                    'place_loc': select_place.place_loc,
                    'latitude': select_place.latitude,
                    'longitude': select_place.longitude,
                    'day_num': select_place.day_num,
                    'trip_id': select_place.trip_id,
                    'cat_id': select_place.cat_id,
                    'notes': select_place.notes,
                    'formatted_date': formatted_date})


@app.route('/delete_place.json', methods=['POST'])
def delete_place():
    """
    Deletes a place by trip_id submitted and just returns a status update to JS.
    """

    place_id = request.form.get('place_id')

    place_to_delete = Place.query.get(int(place_id))

    db.session.delete(place_to_delete)
    db.session.commit()

    return jsonify({'status': 'Deleted'})


@app.route('/edit_place.json', methods=['POST'])
def edit_place():
    """Takes input from the edit form and decides how to update database"""

    place_id = request.form.get('place_id')
    place_name = request.form.get('place_name')
    place_search = request.form.get('place_search')
    visit_day = request.form.get('visit_day')
    day_num, date = visit_day.split(',')
    category = request.form.get('category')
    notes = request.form.get('notes')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    delete_pic = request.form.get('delete')

    place_to_edit = Place.query.get(int(place_id))

    keep_files = ['explore.png', 'eat.png', 'sleep.png', 'transport.png']

    # handles what to do in terms of picture updates
    if 'pic' in request.files:
        # if someone uploads a new picture
        pic_file = request.files['pic']

        # if its an allowed file
        if allowed_file(pic_file.filename):
            # replace the picture for that file if its not a default pic
            if place_to_edit.pic_file not in keep_files:
                # first remove old picture
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                                       place_to_edit.pic_file))

            extension = pic_file.filename.rsplit('.', 1)[1]
            filename = secure_filename('%s.%s' % (place_to_edit.place_id,
                                       extension))
            pic_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # update in database
            place_to_edit.pic_file = filename

    elif delete_pic == 'yes' and place_to_edit.pic_file not in keep_files:
        # make sure to only delete a picture if it isn't a default one.
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                               place_to_edit.pic_file))
        place_to_edit.pic_file = '%s.png' % category

    # below is checking what information was changed and needs to be updated.
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
        # updating the category also updates pic if using a default pic
        if place_to_edit.pic_file in keep_files:
            place_to_edit.pic_file = '%s.png' % category

    if notes != place_to_edit.notes:
        place_to_edit.notes = notes

    if latitude or longitude:
        place_to_edit.latitude = latitude
        place_to_edit.longitude = longitude

    db.session.commit()

    return jsonify({'status': 'Edited'})


@app.route('/publish_trip.json', methods=['POST'])
def publish_trip():
    """toggles if the trip is public or private"""
    trip_id = request.form.get('trip_id')
    target_trip = Trip.query.get(int(trip_id))

    if target_trip.published:
        target_trip.published = False
    else:
        target_trip.published = True

    db.session.commit()

    return jsonify({'status': target_trip.published})


@app.route('/delete_trip.json', methods=['POST'])
def delete_trip():
    """
    Deletes trip from the database. Returns a status and also
    username to take it back to the user's all trips page.
    """
    trip_id = int(request.form.get('trip_id'))

    trip_places = Place.query.filter(Place.trip_id == trip_id).all()
    trip = Trip.query.get(trip_id)

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
        # if trip is not public yet or it isn't the user visiting.
        flash('Sorry! You don\'t have access to this page.')
        return redirect('/')


@app.route('/places_to_map.json')
def return_all_places():
    """
    Passes back info of all places in a trip as json to be
    used to create the Google Maps and markers.
    """
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

        # only have an img_url if picture is not default, changes html to be passed
        default_pics = ['explore.png', 'eat.png', 'sleep.png', 'transport.png']
        if place.pic_file not in default_pics:
            img_url = url_for('uploaded_file', filename=place.pic_file)

            content = """
                    <div id='place-div-%s' class='place-div'>

                    <h5 class='title-%s'>%s</h5>

                    <div style="width:275px;height:212.5px;
                    overflow:hidden;margin: auto" class='place-pic'>
                    <img src='%s' style="width:275px;margin:auto">
                    </div>
                    <p><b>Day %s:</b> %s</p>
                    <p><b>Category:</b> %s</p>
                    <p><b>Place Address:</b> %s</p>
                    <p><b>Notes:</b> %s</p>            
                    </div>
                    """ % (place.place_id, category, title, img_url, day_num, place.date, category,
                           place.place_loc, place.notes)
        else:
            content = """
                    <div id='place-div-%s' class='place-div'>

                    <h5 class='title-%s'>%s</h5>

                    <p><b>Day %s:</b> %s</p>
                    <p><b>Category:</b> %s</p>
                    <p><b>Place Address:</b> %s</p>
                    <p><b>Notes:</b> %s</p>           
                    </div>
                    """ % (place.place_id, category, title, day_num, place.date, category,
                           place.place_loc, place.notes)

        place_info = {'title': title, 'day_num': day_num, 'category': category,
                      'latitude': latitude, 'longitude': longitude,
                      'content': content, 'place_loc': place_loc}

        # add to the dictionary with the key of place_id
        all_places[place.place_id] = place_info

    # jsonify it to be processed in front end
    return jsonify(all_places)


# --------------------------------------------------------------------------- #

if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)

    # DebugToolBarExtension(app)

    app.run(port=5000, host="0.0.0.0")
