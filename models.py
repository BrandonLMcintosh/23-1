

"""Primary DB Class for User object"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

default_pic = "https://st.depositphotos.com/2101611/3925/v/600/depositphotos_39258143-stock-illustration-businessman-avatar-profile-picture.jpg"


class User(db.Model):
    """Defines a user instance"""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"User {u.id} {u.first_name} {u.last_name} {u.image_url}"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True)

    first_name = db.Column(
        db.Text, 
        nullable=False)

    last_name = db.Column(
        db.Text, 
        nullable=False)

    image_url = db.Column(
        db.Text, 
        nullable=False, 
        default=default_pic)


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

    def __repr__(self):
        p = self
        return f'''
        id: {p.id} 
        title: {p.title} 
        content: {p.content} 
        created: {p.created_at} 
        user: {p.user}'''

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.Text,
        nullable=False)

    content = db.Column(
        db.Text,
        nullable=False)

    created_at = db.Column(
        db.Text, 
        nullable=False, 
        default=datetime.now().strftime('%A, %B %d, %Y'))

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey("users.id"))

    user = db.relationship('User', backref=db.backref('posts', cascade="all, delete-orphan"))

    tags = db.relationship(
        'Tag',
        secondary='posts_tags',
        backref='posts')


class PostTag(db.Model):
    """join table for Posts and Tags"""

    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True)

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True)


class Tag(db.Model):
    """Defines Tag. Tags get added to Posts"""

    __tablename__ = "tags"

    def __repr__(self):
        t = self
        return f'id: {t.id} name: {t.name}'


    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True)
    

    @classmethod
    def grab_tags(cls, tag_names):
        """Takes List of tag names and converts to list of corresponding tag objects"""

        tag_list = []

        for name in tag_names:

            tag = cls.query.filter(cls.name==name).first()
            tag_list.append(tag)

        return tag_list


    @classmethod
    def change_tags(cls, post, tags):
        """Compares returned list of tags with post.tags. Adds / removes as necessary"""

        tag_list = cls.grab_tags(tags)

        for tag in tag_list:

            if tag not in post.tags:

                post.tags.append(tag)

        for tag in post.tags:

            if tag not in tag_list:

                post.tags.remove(tag)

        db.session.add(post)
        db.session.commit()

        return
        

def connect_db(app):
    """connects to the db"""
    db.app = app
    db.init_app(app)