"""Primary DB Class for User object"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType

db = SQLAlchemy()


def connect_db(app):
    """connects to the db"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Defines a user instance"""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"User {u.first_name} {u.last_name} {u.image_url}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    image_url = db.Column(URLType)
