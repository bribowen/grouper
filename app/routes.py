#!/usr/bin/env python
from app import app
from flask import flash, redirect, render_template, url_for, session
from app.forms import LoginForm
import os

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
