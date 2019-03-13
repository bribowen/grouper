#!/usr/bin/env python
import os
from flask import flash, request, redirect, render_template, request, session, url_for, json
from flask_login import current_user, login_user, logout_user, login_manager, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import Profile
from werkzeug.urls import url_parse
#from flaskext.mysql import MySQL
"""mysql = MySQL()

#MySQL configs
app.config['MYSQL_DATABASE_USER'] = 'grouper'
app.config['MYSQL_DATABASE_PASSWORD'] = 'grouper'
app.config['MYSQL_DATABASE_DB'] = 'grouper'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()"""

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in College Station!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'I smell funny!'
    }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Profile.query.filter_by(email_address=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #TODO: figure out next_page issue
        """next_page = request.args.get('next')
        print(str(next_page))
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')"""
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Profile(uin=form.uin.data, email_address=form.email.data, first_name=form.fname.data,
        last_name=form.lname.data, user_persona_type=form.persona.data, primary_contact=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return 'The about page'

@app.route('/user/<username>')
def show_user_profile(uin):
    #show the user profile for that user
    return 'User %s' % uin

@app.route('/posts')
def posts():
    return 'The posts page'

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    #show the post with the given id
    return 'Post %d' % post_id
