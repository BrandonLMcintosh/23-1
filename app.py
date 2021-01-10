"""Blogly application."""
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "SuperSecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def index():
    return redirect("/users")


@app.route('/users')
def users_get():
    return render_template("user_list.html.j2")


@app.route('/users/new')
def new_user():
    return render_template("new_user.html.j2")


@app.route('/users/new', methods=["POST"])
def users_post():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_get(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user.html.j2", user=user)


@app.route('/users/<int:user_id>/edit')
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.commit()
    return redirect(f'users/{user_id}')


@app.route('/users/<int:user_id>/delete')
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    
