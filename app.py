"""Blogly application."""
from re import template
from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag
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
app.create_jinja_environment()


toolbar = DebugToolbarExtension(app)
connect_db(app)
# db.drop_all()
db.create_all()


###########################################################################################################
#####INDEX#################################################################################################
###########################################################################################################


@app.route('/')
def index():

    return redirect('/posts')


###########################################################################################################
#####USERS#################################################################################################
###########################################################################################################


@app.route('/users')
def users_list():

    users = User.query.order_by(User.first_name).all()
    return render_template("users/list.html.j2", users=users)


@app.route('/users/new', methods=["GET", "POST"])
def users_new():

    if request.method == "GET":

        return render_template("users/new.html.j2", back='/users')

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


@app.route('/users/<int:user_id>')
def users_get(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("users/get.html.j2", user=user, back='/users')


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def users_edit(user_id):

    user = db.session.query(User).get_or_404(user_id)

    if request.method == "GET":
        
        return render_template("users/edit.html.j2", user=user, back=f'/users/{user_id}')
    
    elif request.method == "POST":

        db.session.add(user)
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.image_url = request.form["image_url"]
        db.session.commit()

        return redirect(f'/users/{user_id}')
    
    else: 

        return redirect(f'/users')


@app.route('/users/<int:user_id>/delete')
def users_delete(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


###########################################################################################################
#####POSTS#################################################################################################
###########################################################################################################


@app.route('/posts')
def posts_list():

    posts = db.session.query(Post).order_by(Post.id.desc()).limit(5)

    return render_template("posts/list.html.j2", posts=posts)


@app.route('/posts/new/<int:user_id>', methods=["GET", "POST"])
def posts_new(user_id):

    user = User.query.get_or_404(user_id)

    if request.method == "GET":

        return render_template('posts/new.html.j2', user=user, back=f'/users/{user_id}')

    elif request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        created_at = datetime.now()

        post = Post(title=title, content=content, created_at=created_at, user_id=user_id)

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user_id}')

    else:
        
        return redirect(f'/posts')


@app.route('/posts/<int:post_id>')
def posts_get(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('posts/get.html.j2', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def posts_edit(post_id):
    """POST route for user post edit. Doesn't change post.created_at or post.user"""

    post = Post.query.get(post_id)

    if request.method == "GET":

        return render_template('posts/edit.html.j2', post=post, back=f'/posts/{post_id}')

    elif request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        updated_at = datetime.now().strftime('%A, %B %d, %Y')

        post.title = title
        post.content = content
        post.updated_at = updated_at

        db.session.add(post)
        db.session.commit()

        return redirect(f'/posts/{post_id}')
    
    else:

        return redirect(f'/users')


@app.route('/posts/<int:post_id>/delete')
def posts_delete(post_id):
    """Grab post from DB, delete from DB"""

    post = Post.query.get(post_id)
    user = post.user_id
    
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user}')


##########################################################################################################
#####TAGS#################################################################################################
##########################################################################################################


@app.route('/tags')
def tags_list():

    tags = Tag.query.all()

    return render_template('tags/list.html.j2', tags=tags)


@app.route('/tags/new', methods=["GET", "POST"])
def tags_new():

    if request.method == "GET":

        return render_template('tags/new.html.j2', back="/tags")

    elif request.method == "POST":

        name = request.form['name']
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')
        
    else: 

        return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tags_get(tag_id):

    tag = Tag.query.get(tag_id)

    return render_template('tags/get.html.j2', tag=tag, back='/tags')


@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def tags_edit(tag_id):

    tag = Tag.query.get(tag_id)
    
    if request.method == "GET":

        return render_template('tags/edit.html.j2', tag=tag, back=f'/tags/{tag.id}')

    elif request.method == "POST":

        name = request.form['name']
        tag.name = name
        db.session.add(tag)
        db.session.commit()

        return redirect(f'/tags/{tag.id}')

    else:

        return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete')
def tags_delete(tag_id):

    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')


###########################################################################################################
#####CATCH#################################################################################################
###########################################################################################################

@app.errorhandler(404)
def page_not_found(error):
    """redirect to a safe page with a back button"""

    return render_template('root/404.html.j2', error=error, back=f'/users')
