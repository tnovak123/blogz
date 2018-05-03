from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    if len(User.query.all()) == 0:
        flash("There are no users in the database.")
        return redirect('/signup')
    else:
        users = User.query.all()
        return render_template('index.html', title="Blogz", users=users)

@app.route('/post')
def post():
    pid = request.args.get('post_id')
    post = Post.query.filter_by(id=pid).first()
    users = User.query.all()
    return render_template('post.html', title='View one post', users=users, post=post)

@app.route('/allposts')
def allposts():
    if len(Post.query.all()) == 0:
        flash("There are no blogs to display.")
        return redirect('/login')
    else:
        posts = Post.query.all()
        users = User.query.all()
        return render_template('allposts.html', title='View all posts.', posts=posts, users=users)
    #page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.timestamp.desc()).paginate(
    #    page, app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for('explore', page=posts.next_num) \
    #    if posts.has_next else None
    #prev_url = url_for('explore', page=posts.prev_num) \
    #    if posts.has_prev else None
    #return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('newpost'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
            
        login_user(user)
        flash('Login requested for user {}.'.format(form.username.data))
        return redirect(url_for('newpost'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a register user!')
        return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up!', form=form)

@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('allposts'))

    return render_template('newpost.html', Title='New Post', form=form)

@app.route('/user')
def user():
    user = User.query.filter_by(id=request.args.get('user_id')).first()
    users = User.query.all()
    posts = Post.query.all()
    return render_template('singleUser.html', posts=posts, user=user, users=users)