"""Models for Itinerary Mapper Project"""

from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()

###############################################################################
# Model definitions


class User(db.Model):
    """User of itinerary-mapper website."""
    __tablename__ = 'users'

    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Helpful representation when printed"""

        return '<User username=%s>' % (self.username)


class Trip(db.Model):
    """Trip of a user"""
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_name = db.Column(db.String(256), nullable=False)
    general_loc = db.Column(db.String(256), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    username = db.Column(db.String(64),
                        db.ForeignKey('users.username'),
                        nullable=False)

    user = db.relationship('User',
                           backref=db.backref('trips',
                                              order_by=trip_id))

    def __repr__(self):
        """Helpful representation when printed."""

        return "<Trip trip_id=%s trip_name=%s>" % (self.trip_id,
                                                   self.trip_name)


class Day(db.Model):
    """Day of a trip"""
    __tablename__ = 'days'

    day_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    day_num = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)

    trip = db.relationship('Trip',
                           backref=db.backref('days',
                                              order_by=day_id))

    def __repr__(self):
        """Helpful representation when printed."""

        return "<Day day_id=%s>" % (self.day_id)


class Category(db.Model):
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
    place_name = db.Column(db.String(256), nullable=False)
    place_loc = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    day_id = db.Column(db.Integer,
                       db.ForeignKey('days.day_id'),
                       nullable=False)
    #  iffy about having trip_id
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)
    cat_id = db.Column(db.String(16),
                       db.ForeignKey('categories.cat_id'),
                       nullable=False)
    notes = db.Column(db.Text, nullable=True)

    day = db.relationship('Day', backref=db.backref('places',
                                                    order_by=place_id))
    # iffy about having this relationship
    trip = db.relationship('Trip',
                           backref=db.backref('places',
                                              order_by=place_id))

    def __repr__(self):
        """Helpful representation when printed."""

        display = "<Place place_id=%s place_name=%s day_id=%s cat_id=%s>"
        return display % (self.place_id,
                          self.place_name,
                          self.day_id,
                          self.cat_id)


# use this when testing
def example_data():
    """Create example data for the test database."""

    # example users
    liz = User(name='Elizabeth Lemon', username='lizlemon', password='pizza')
    leslie = User(name='Leslie Knope', username='l.k.pawnee', password='parksandrec')

    # example trips
    portland = Trip(trip_name='A Weekend in Portland', general_loc='Portland, Oregon',
                    latitude=45.523062, longitude=-122.676482, username='lizlemon')
    vancouver = Trip(trip_name='Vancouver for a Day', username='lizlemon')
    taiwan = Trip(trip_name='Taiwan', general_loc='Taiwan', latitude=23.697810,
                  longitude=120.960515, username='l.k.pawnee')

    # example days
    pdx_day_one = Day(day_num=1, date=datetime.datetime(2016, 7, 5, 0, 0), trip_id=1)
    pdx_day_two = Day(day_num=2, date=datetime.datetime(2016, 7, 6, 0, 0), trip_id=1)
    bcn_day_one = Day(day_num=1, date=datetime.datetime(2016, 1, 21, 0, 0), trip_id=2)
    tw_day_one = Day(day_num=1, date=datetime.datetime(2016, 10, 1, 0, 0), trip_id=3)
    tw_day_two = Day(day_num=2, date=datetime.datetime(2016, 10, 2, 0, 0), trip_id=3)
    tw_day_three = Day(day_num=3, date=datetime.datetime(2016, 10, 3, 0, 0), trip_id=3)

    # example categories
    eat = Category(cat_id='eat')
    sleep = Category(cat_id='sleep')
    explore = Category(cat_id='explore')
    transport = Category(cat_id='transport')

    # example places
    pdx_place_one = Place(place_name='Saturday Market',
                          place_loc="Portland Saturday Market, Southwest Naito Parkway, Portland, OR",
                          latitude=45.522630, longitude=-122.670025,
                          day_id=1, trip_id=1, cat_id='explore')
    pdx_place_two = Place(place_name='Blue Star Donuts',
                          place_loc="Blue Star Donuts, Southwest Washington Street, Portland, OR",
                          latitude=45.520690, longitude=-122.678911,
                          day_id=1, trip_id=1, cat_id='eat')
    pdx_place_three = Place(place_name='Ace Hotel',
                            place_loc="Ace Hotel Portland, Southwest Stark Street, Portland, OR",
                            latitude=45.521089, longitude=-122.677568,
                            day_id=1, trip_id=1, cat_id='sleep')
    pdx_place_four = Place(place_name='Oregon Historical Society',
                           place_loc="Oregon Historical Society, Southwest Park Avenue, Portland, OR",
                           latitude=45.515738, longitude=-122.683275,
                           day_id=2, trip_id=1, cat_id='explore')
    pdx_place_five = Place(place_name='Pine State Biscuits',
                           place_loc="Pine State Biscuits, Northeast Schuyler Street, Portland, OR",
                           latitude=45.535732, longitude=-122.644831,
                           day_id=2, trip_id=1, cat_id='eat')
    bcn_place_one = Place(place_name='Kirin Dim Sum',
                          place_loc="Kirin Restaurant, Alberni Street, Vancouver, BC, Canada",
                          latitude=49.288621, longitude=-123.128863,
                          day_id=3, trip_id=2, cat_id='eat')
    bcn_place_two = Place(place_name='Vancouver Library',
                          place_loc="Vancouver Public Library- Central Branch, West Georgia Street, Vancouver, BC, Canada",
                          latitude=49.285096, longitude=-123.122143,
                          day_id=3, trip_id=2, cat_id='explore')
    tw_place_one = Place(place_name='Taiwan National Palace Museum',
                         place_loc="National Palace Museum, Section 2, Zhishan Road, Shilin District, Taipei City, Taiwan",
                         latitude=25.102355, longitude=121.548493,
                         day_id=4, trip_id=3, cat_id='explore')
    tw_place_two = Place(place_name='Kaohsiung Station',
                         place_loc="Kaohsiung Station, Sanmin District, Kaohsiung City, Taiwan",
                         latitude=22.639761, longitude=120.302107,
                         day_id=5, trip_id=3, cat_id='transport')
    tw_place_three = Place(place_name='Din Tai Fung',
                           place_loc="Din Tai Fung, City Hall Road, Xinyi District, Taipei City, Taiwan",
                           latitude=25.028702, longitude=121.576957,
                           day_id=6, trip_id=3, cat_id='eat')

    db.session.add_all([liz, leslie, portland, vancouver, taiwan,
                        pdx_day_one, pdx_day_two, bcn_day_one, tw_day_one,
                        tw_day_two, tw_day_three, eat, sleep, explore,
                        transport, pdx_place_one, pdx_place_two, pdx_place_three,
                        pdx_place_four, pdx_place_five, bcn_place_one,
                        bcn_place_two, tw_place_one, tw_place_two, tw_place_three])

    db.session.commit()


# Helper functions
def connect_to_db(app):
    """Connect the database to Flask app"""

    #Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///itineraries'
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    #can run module interactiviely and work with database directly

    from server import app
    connect_to_db(app)
    print 'Connected to DB.'
