from unittest import TestCase
from app import app
from models import db, User


class Test_App(TestCase):
    """Tests for 4 routes in app"""

    def setUp(self):
        user = User(first_name="Thomas", last_name="Wright", image_url="FAKE IMAGE")
        db.session.add(user)
        db.session.commit()

    
    def tearDown(self):
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        db.session.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")


    def test_get_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")


    def test_get_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertIn("Thomas Wright", html)
    

    def test_post_users(self):
        first_name = "John"
        last_name = "Wayne"
        image_url = "NO IMAGE"
        with app.test_client() as client:
            client.post('/users/new', data=dict(first_name=first_name, last_name=last_name, image_url=image_url), follow_redirects=True)
        user = User.query.filter_by(first_name=first_name).first()
        self.assertEqual(user.first_name, first_name)
        db.session.delete(user)
        db.session.commit()


    def test_get_user(self):
        user = User.query.get(1)
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)
            self.assertIn(user.full_name, html)

        
    def test_post_edit_user(self):
        new_first_name = "New"
        new_last_name = "Name"
        new_image_url = "DONKEY"
        resp = None
        with app.test_client() as client:
            resp = client.post('/users/1/edit', data=dict(first_name=new_first_name, last_name=new_last_name, image_url=new_image_url), follow_redirects=True)
        
        html = resp.get_data(as_text=True)
        user = User.query.get(1)
        self.assertIn(user.full_name, html)
        self.assertEqual(user.first_name, new_first_name)


    def test_get_user_delete(self):
        user = User.query.get(1)
        with app.test_client() as client:
            resp = client.get("/users/1/delete")
            html = resp.get_data(as_text=True)
            self.assertNotIn(user.full_name, html)
