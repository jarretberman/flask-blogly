from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add Sample User"""

        User.query.delete()

        user = User(first_name="bob", last_name="jeff")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """clean up if queries fail"""

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code= 200)
            self.assertIn('bob', html)

    def test_user_page(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code= 200)
            self.assertIn('bob', html)

    def test_user_form(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code= 200)
            self.assertIn('<form>', html)

    def test_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")
