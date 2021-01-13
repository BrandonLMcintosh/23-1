"""Blogly application."""
from re import template
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "SuperSecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()
##################################
### START INVIDIDUAL GET ROUTES ##
##################################
@app.route('/')
def index():
    """REDIRECTS IMMEDIATELY TO /USERS"""
    return redirect("/users")


@app.route('/users')
def users_get():
    """GET ROUTE FOR USER LIST (INDEX)"""

    users = User.query.order_by(User.first_name).all()
    return render_template("root/user_list.html.j2", users=users)


@app.route('/users/<int:user_id>')
def users_get_user(user_id):
    """GET ROUTE FOR INDIVIDUAL USER"""

    user = User.query.get_or_404(user_id)

    return render_template("user/user.html.j2", user=user)

##################################
##### START  GET/POST ROUTES #####
##################################


@app.route('/users/new', methods=["GET", "POST"])
def users_post():
    """POST ROUTE FOR NEW USER"""

    if request.method == "GET":

        return render_template("user/new_user.html.j2")

    elif request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"] or None

        user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)

        db.session.add(user)
        db.session.commit()

        return redirect(f'/users/{user.id}')

    else:

        return redirect('/users')


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def users_user_edit(user_id):
    """POST/GET ROUTE FOR USER EDIT"""

    user = db.session.query(User).get_or_404(user_id)

    if request.method == "GET":
        
        return render_template("user/edit_user.html.j2", user=user)
    
    elif request.method == "POST": 

        db.session.add(user)
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.image_url = request.form["image_url"]
        db.session.commit()

        return redirect(f'/users/{user_id}')
    
    else: 

        return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=["GET", "POST"])
def user_posts_edit(user_id, post_id):
    """POST route for user post edit. Doesn't change post.created_at or post.user"""

    user = db.session.query(User).get(user_id)
    post = db.session.query(Post).get(post_id)

    if request.method == "GET":

        return render_template('post/post.html.j2', user=user, post=post)

    elif request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        updated_at = datetime.utcnow()

        post.title = title
        post.content = content
        post.updated_at = updated_at

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user_id}/posts/{post_id}')
    
    else:

        return redirect(f'/users/{user_id}/posts/{post_id}')

##################################
##### START  DELETE ROUTES #######
##################################


@app.route('/users/<int:user_id>/delete')
def users_user_delete(user_id):
    """GET ROUTE FOR USER DELETE"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/<int:post_id>/delete')
def user_posts_delete(user_id, post_id):
    pass
    # need to do: 
    #     -add delete button to user post template
    #     -add logic to remove from db and redirect
