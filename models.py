

"""Primary DB Class for User object"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime

db = SQLAlchemy()

default_pic = "https://st.depositphotos.com/2101611/3925/v/600/depositphotos_39258143-stock-illustration-businessman-avatar-profile-picture.jpg"


class User(db.Model):
    """Defines a user instance"""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"User {u.id} {u.first_name} {u.last_name} {u.image_url}"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=default_pic)

    posts = db.relationship("Post", backref="users")


    @classmethod
    def query_by_first_name(cls):
        """Class method query to return all users ordered alphabetically"""

        return cls.query.order_by(cls.first_name).all()

    @property
    def full_name(self):
        """Returnes the full name of the user"""

        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Defines post. User to many posts, post to one user"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.now())
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

def connect_db(app):
    """connects to the db"""
    db.app = app
    db.init_app(app)
