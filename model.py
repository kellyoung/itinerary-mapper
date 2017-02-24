"""Models for Itinerary Mapper Project"""

from flask_sqlalchemy import SQLAlchemy

import datetime

import bcrypt

db = SQLAlchemy()

###############################################################################
# Model definitions


class User(db.Model):
    """User of itinerary-mapper website."""
    __tablename__ = 'users'

    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        """Helpful representation when printed"""

        return '<User username=%s>' % (self.username)



class Trip(db.Model):
    """Trip of a user"""
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_name = db.Column(db.String(256), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    general_loc = db.Column(db.String(256), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    viewport = db.Column(db.Text, nullable=True)
    username = db.Column(db.String(64),
                         db.ForeignKey('users.username'),
                         nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship('User',
                           backref=db.backref('trips',
                                              order_by=trip_id))

    def __repr__(self):
        """Helpful representation when printed."""

        return "<Trip trip_id=%s trip_name=%s>" % (self.trip_id,
                                                   self.trip_name)


class PlaceCategory(db.Model):
    """Category that days can belong to"""

    __tablename__ = 'categories'

    cat_id = db.Column(db.String(16),
                       nullable=False,
                       primary_key=True)

    def __repr__(self):
        """Helpful representation when printed."""

        return "<Category cat_id=%s>" % self.cat_id


class Place(db.Model):
    """Place of a day"""
    __tablename__ = 'places'

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    place_name = db.Column(db.Unicode(256), nullable=False)
    place_loc = db.Column(db.Unicode(256), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    day_num = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)
    cat_id = db.Column(db.String(16),
                       db.ForeignKey('categories.cat_id'),
                       nullable=False)
    notes = db.Column(db.UnicodeText, nullable=True)
    pic_file = db.Column(db.Text, nullable=True)
    trip = db.relationship('Trip',
                           backref=db.backref('places',
                                              order_by=place_id))

    def __repr__(self):
        """Helpful representation when printed."""

        display = "<Place place_id=%s place_name=%s date=%s cat_id=%s>"
        return display % (self.place_id,
                          self.place_name,
                          self.date.strftime("%B %d, %Y"),
                          self.cat_id)


# create the categories
def create_cat_table():
    """create the table for place categories"""

    # example categories
    eat = PlaceCategory(cat_id='eat')
    sleep = PlaceCategory(cat_id='sleep')
    explore = PlaceCategory(cat_id='explore')
    transport = PlaceCategory(cat_id='transport')

    db.session.add_all([eat, sleep, explore, transport])
    db.session.commit()


# use this when testing
def example_data():
    """Create example data for the test database."""

    # example users
    password = 'pizza'
    hashed_pw = bcrypt.hashpw(str(password), bcrypt.gensalt())
    liz = User(name='Elizabeth Lemon', username='lizlemon', password=hashed_pw)

    # example trips
    portland = Trip(trip_name='A Weekend in Portland', start_date=datetime.date(2016, 7, 5),
                    end_date=datetime.date(2016, 7, 6), general_loc='Portland, Oregon',
                    latitude=45.523062, longitude=-122.676482,
                    viewport='{"south":45.432393,"west":-122.83699519999999,"north":45.6524799,"east":-122.4718489}',
                    published=True, username='lizlemon')

    # example categories
    eat = PlaceCategory(cat_id='eat')
    sleep = PlaceCategory(cat_id='sleep')
    explore = PlaceCategory(cat_id='explore')
    transport = PlaceCategory(cat_id='transport')

    # example places
    pdx_place_one = Place(place_name='Saturday Market',
                          place_loc="Portland Saturday Market, Southwest Naito Parkway, Portland, OR",
                          latitude=45.522630, longitude=-122.670025, day_num=1,
                          date=datetime.date(2016, 7, 5), trip_id=1, cat_id='explore',
                          notes='nice place to have lunch.', pic_file='/uploads/explore.png')
    pdx_place_two = Place(place_name='Blue Star Donuts',
                          place_loc="Blue Star Donuts, Southwest Washington Street, Portland, OR",
                          latitude=45.520690, longitude=-122.678911, day_num=1,
                          date=datetime.date(2016, 7, 5), trip_id=1, cat_id='eat', pic_file='/uploads/eat.png')
    pdx_place_three = Place(place_name='Ace Hotel',
                            place_loc="Ace Hotel Portland, Southwest Stark Street, Portland, OR",
                            latitude=45.521089, longitude=-122.677568, day_num=1,
                            date=datetime.date(2016, 7, 5), trip_id=1, cat_id='sleep',
                            notes='nice hotel', pic_file='/uploads/sleep.png')
    pdx_place_four = Place(place_name='Oregon Historical Society',
                           place_loc="Oregon Historical Society, Southwest Park Avenue, Portland, OR",
                           latitude=45.515738, longitude=-122.683275, day_num=2,
                           date=datetime.date(2016, 7, 6), trip_id=1,
                           cat_id='explore', pic_file='/uploads/explore.png')

    db.session.add_all([liz, portland, eat, sleep, explore, transport,
                        pdx_place_one, pdx_place_two, pdx_place_three,
                        pdx_place_four])
    db.session.add_all([eat, sleep, explore, transport])

    db.session.commit()


# Helper functions
def connect_to_db(app, db_uri='postgresql:///itineraries'):
    """Connect the database to Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    #can run module interactiviely and work with database directly
    from server import app
    connect_to_db(app)
    print 'Connected to DB.'
