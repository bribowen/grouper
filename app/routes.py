#!/usr/bin/env python
import os
from flask import flash, redirect, render_template, request, session, url_for, json
from app import app
from app.models import Project, Profile
from app.forms import LoginForm, SignupForm
from flaskext.mysql import MySQL

mysql = MySQL()

#MySQL configs
app.config['MYSQL_DATABASE_USER'] = 'grouper'
app.config['MYSQL_DATABASE_PASSWORD'] = 'grouper'
app.config['MYSQL_DATABASE_DB'] = 'grouper'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Brian'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	flash('Login requested for user {}, remember_me={}'.format(
    		form.username.data, form.remember_me.data))
    	return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    _uin = form.uin.data
    _firstName = form.fname.data
    _lastName = form.lname.data
    _persona = form.persona.data
    _phone = form.phone.data
    _email = form.email.data
    _password = form.password.data

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()

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
