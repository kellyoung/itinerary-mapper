import unittest

import datetime

from server import app
from model import db, example_data, connect_to_db, User, Trip, Place, Category

import json


class ItineraryTests(unittest.TestCase):
    """Tests for my site"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage_no_login(self):
        result = self.client.get("/")
        self.assertIn("CREATE ACCOUNT", result.data)


class ItineraryDatabaseTests(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Set up the database before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testitinerarydb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_success_login(self):
        result = self.client.post("/login",
                                  data={"username": "lizlemon",
                                        "password": "pizza"},
                                  follow_redirects=True)
        self.assertIn('Welcome,', result.data)
        self.assertIn('NAME YOUR TRIP:', result.data)
        self.assertIn('All Trips', result.data)
        self.assertNotIn('The username and password do not exist. Try again.', result.data)

    def test_failed_login(self):
        result = self.client.post("/login",
                                  data={"username": "leslieknope",
                                        "password": 'pawneepride'},
                                  follow_redirects=True)
        self.assertNotIn('Welcome,', result.data)
        self.assertIn('The username and password do not exist. Try again.', result.data)

    def test_no_input_login(self):
        result = self.client.post("/login", follow_redirects=True)
        self.assertNotIn('Welcome', result.data)
        self.assertIn('enter a username', result.data)

    def test_wrong_pw_login(self):
        result = self.client.post("/login",
                                  data={"username": "lizlemon",
                                        "password": 'pawneepride'},
                                  follow_redirects=True)
        self.assertIn('Incorrect Password.', result.data)

    def test_success_create_user(self):
        result = self.client.post("/create_user",
                                  data={"username": "ronswanson",
                                        "password": "bacon",
                                        "name": "Ron Swanson"},
                                  follow_redirects=True)
        self.assertIn('successfully created. You are now signed in.', result.data)
        self.assertNotIn('Please try again.', result.data)

    def test_failed_create_user(self):
        result = self.client.post("/create_user",
                                  data={"username": "lizlemon",
                                        "password": "bacon",
                                        "name": "Ron Swanson"},
                                  follow_redirects=True)
        self.assertNotIn('successfully created. Please log in.', result.data)
        self.assertIn('Please try again.', result.data)

    def test_reprs(self):
        """Test the reprs of models"""

        user_repr = User.query.get('lizlemon').__repr__()
        assert ('<User username=lizlemon>' == user_repr)

        trip_repr = Trip.query.get(1).__repr__()
        assert ("<Trip trip_id=1 trip_name=A Weekend in Portland>" == trip_repr)

        cat_repr = Category.query.get('eat').__repr__()
        assert ("<Category cat_id=eat>" == cat_repr)

        place_repr = Place.query.get(1).__repr__()
        assert ("<Place place_id=1 place_name=Saturday Market date=July 05, 2016 cat_id=explore>" == place_repr)

    def test_places_to_map_json(self):
        """ Test json of places_to_map """

        result = self.client.get('/places_to_map.json',
                                 query_string={'trip_id': '1'})

        places_json = json.loads(result.data)
        assert 'Saturday Market' in places_json['1']['title']


class ItineraryInSessionTests(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        connect_to_db(app, "postgresql:///testitinerarydb")

        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'lizlemon'

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_all_trips_page(self):
        """Test All Trips page."""
        result = self.client.get("/lizlemon/trips", follow_redirects=True)
        self.assertNotIn('You do not have access to this page.', result.data)
        self.assertIn('A Weekend in Portland', result.data)

    def test_create_trip_page(self):
        """Test a specific trip page."""
        result = self.client.get("/create_trip/lizlemon/1", follow_redirects=True)
        self.assertNotIn('You do not have access to this page.', result.data)
        self.assertIn('Saturday Market', result.data)
        self.assertIn('Blue Star Donuts', result.data)

    def test_logout(self):
        """Test if logout works"""
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn('Logged out of', result.data)

    def test_map_view_page(self):
        """Test Map View if user in session"""
        result = self.client.get("/lizlemon/1/mapview", follow_redirects=True)
        self.assertIn('MAP FILTERS:', result.data)

    def test_create_trip_json(self):
        """ Test create trip json """

        result = self.client.post('/create_trip.json',
                                  data={'tripname': 'Test Trip',
                                        'from': '12/06/2016',
                                        'to': '12/09/2016',
                                        'latitude': 45.523062,
                                        'longitude': -122.676482,
                                        'loc_name': 'Test, Location',
                                        'viewport': '{"south":45.432393,"west":\
                                        -122.83699519999999,"north":\
                                        45.6524799,"east":-122.4718489}'
                                        })

        trip_json = json.loads(result.data)
        assert 'success' in trip_json['status']

    def test_trip_loc_info_json(self):
        """ Test json of trip_loc_info """

        result = self.client.get('/trip_loc_info.json',
                                 query_string={'trip_id': '1'})

        trip_json = json.loads(result.data)
        assert '{"south":45.432393,"west":-122.83699519999999,"north":45.6524799,"east":-122.4718489}' in trip_json['viewport']

    def test_edit_place_info_json(self):
        """ Test json of edit_place_info"""

        result = self.client.get('/edit_place_info.json',
                                 query_string={'place_id': '1'})

        places_json = json.loads(result.data)
        assert 'explore' in places_json['cat_id']

    def test_delete_place_json(self):
        """ Test json of delete_place"""

        result = self.client.post('/delete_place.json',
                                  data={'place_id': '1'})

        delete_json = json.loads(result.data)
        assert 'Deleted' in delete_json['status']

    def test_publish_trip_json(self):
        """ Test json of publish_trip"""

        result = self.client.post('/publish_trip.json',
                                  data={'trip_id': '1'})

        self.assertTrue(result.status)

    def test_delete_trip_json(self):
        """ Test json of delete_trip"""

        result = self.client.post('/delete_trip.json',
                                  data={'trip_id': '1'})

        delete_json = json.loads(result.data)
        assert 'success' in delete_json['status']


class ItineraryNoSessionTests(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

        connect_to_db(app, "postgresql:///testitinerarydb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_all_trips_page(self):
        """Test that user can't see all trips page when logged out."""

        result = self.client.get("/lizlemon/trips", follow_redirects=True)
        self.assertIn('You do not have access to this page.', result.data)
        self.assertNotIn('By:', result.data)

    def test_create_trip_page(self):
        """Test a specific trip page."""
        result = self.client.get("/create_trip/lizlemon/1", follow_redirects=True)
        self.assertIn('You do not have access to this page.', result.data)
        self.assertNotIn('Saturday Market', result.data)
        self.assertNotIn('Blue Star Donuts', result.data)

    def test_map_view_page(self):
        """Test Map View if user not in session but published"""
        result = self.client.get("/lizlemon/1/mapview")
        self.assertIn('MAP FILTERS:', result.data)

    def test_map_view_page(self):
        """Test Map View if user not in session and not published"""
        target_trip = Trip.query.get(1)
        target_trip.published = False
        db.session.commit()
        result = self.client.get("/lizlemon/1/mapview", follow_redirects=True)
        self.assertNotIn('MAP FILTERS:', result.data)
        self.assertIn('Sorry!', result.data)


if __name__ == "__main__":
    unittest.main()
