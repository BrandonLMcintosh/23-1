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
    """REDIRECTS IMMEDIATELY TO /USERS"""
    return redirect("/users")


@app.route('/users')
def users_get():
    """GET ROUTE FOR USER LIST (INDEX)"""

    users = User.query.all()
    return render_template("user_list.html.j2", users=users)


@app.route('/users/new')
def users_new():
    """GET ROUTE FOR NEW USER FORM"""
    
    return render_template("new_user.html.j2")


@app.route('/users/new', methods=["POST"])
def users_post():
    """POST ROUTE FOR NEW USER"""

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
def users_get_user(user_id):
    """GET ROUTE FOR INDIVIDUAL USER"""

    user = User.query.get_or_404(user_id)
    return render_template("user.html.j2", user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit_get(user_id):
    """GET ROUTE FOR USER EDIT"""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html.j2", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_edit_post(user_id):
    """POST ROUTE FOR USER EDIT"""

    user = User.query.get_or_404(user_id)
    db.session.add(user)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.commit()



@app.route('/users/<int:user_id>/delete')
def users_delete_user(user_id):
    """GET ROUTE FOR USER DELETE"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
