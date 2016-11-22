import unittest

from server import app
from model import db, example_data, connect_to_db


class ItineraryTests(unittest.TestCase):
    """Tests for my site"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage_no_login(self):
        result = self.client.get("/")
        self.assertIn("Create an Account", result.data)
        self.assertNotIn("Logout", result.data)


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
        self.assertIn('Create Trip', result.data)
        self.assertIn('Go to Trips', result.data)
        self.assertNotIn('The username and password do not exist. Try again.', result.data)

    def test_failed_login(self):
        result = self.client.post("/login",
                                  data={"username": "leslieknope",
                                        "password": "pawneepride"},
                                  follow_redirects=True)
        self.assertNotIn('Welcome,', result.data)
        self.assertIn('The username and password do not exist. Try again.', result.data)

    def test_success_create_user(self):
        result = self.client.post("/create_user",
                                  data={"username": "ronswanson",
                                        "password": "bacon",
                                        "name": "Ron Swanson"},
                                  follow_redirects=True)
        self.assertIn('successfully created. Please log in.', result.data)
        self.assertNotIn('Please try again.', result.data)

    def test_failed_create_user(self):
        result = self.client.post("/create_user",
                                  data={"username": "lizlemon",
                                        "password": "bacon",
                                        "name": "Ron Swanson"},
                                  follow_redirects=True)
        self.assertNotIn('successfully created. Please log in.', result.data)
        self.assertIn('Please try again.', result.data)


class ItineraryInSessionTests(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 'test'

    def test_all_trips_page(self):
        """Test All Trips page."""

        result = self.client.get("/important")
        self.assertIn("You are a valued user", result.data)


class ItineraryNoSessionTests(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_important_page(self):
        """Test that user can't see important page when logged out."""

        result = self.client.get("/important", follow_redirects=True)
        self.assertNotIn("You are a valued user", result.data)
        self.assertIn("You must be logged in", result.data)


if __name__ == "__main__":
    unittest.main()
