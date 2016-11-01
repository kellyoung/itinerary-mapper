"""Models for Itinerary Mapper Project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

###############################################################################
# Model definitions


class User(db.Model):
    """User of itinerary-mapper website."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Helpful representation when printed"""

        return '<User user_id=%s name=%s>' % (self.user_id, self.name)


class Trip(db.Model):
    """Trip of a user"""
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_name = db.Column(db.String(128), nullable=False)
    general_loc = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
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


class Place(db.Model):
    """Place of a day"""
    __tablename__ = 'places'

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    place_name = db.Column(db.String(128), nullable=False)
    place_loc = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    day_id = db.Column(db.Integer,
                       db.ForeignKey('days.day_id'),
                       nullable=False)
    cat_id = db.Column(db.String(16),
                       db.ForeignKey('categories.cat_id'),
                       nullable=False)
    notes = db.Column(db.Text, nullable=True)

    day = db.relationship('Day', backref=db.backref('places',
                                                    order_by=place_id))
    category = db.relationship('Category',
                               backref=db.backref('places',
                                                  order_by=place_id))

    def __repr__(self):
        """Helpful representation when printed."""

        display = "<Place place_id=%s place_name=%s day_id=%s cat_id=%s>"
        return display % (self.place_id,
                          self.place_name,
                          self.day_id,
                          self.cat_id)


class Category(db.Model):
    """Category that days can belong to"""
    cat_id = db.Column(db.String(16),
                       nullable=False)

    def __repr__(self):
        """Helpful representation when printed."""

        return "<Category cat_id=%s" % self.cat_id


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
