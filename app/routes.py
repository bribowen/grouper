#!/usr/bin/env python
from app import app
from flask import flash, redirect, render_template, url_for
from app.forms import LoginForm
import os

#Class to use for individual projects. Takes in the poster's first/last name, the project name,
#the project type (individual or for a class), and a brief description.
class Project:
    def __init__(self, post_id, posterfname, posterlname, projname, projtype, description):
        self.post_id = post_id
        self.posterfname = posterfname
        self.posterlname = posterlname
        self.projname = projname
        self.type = projtype
        self.description = description
    #Method for updating parts of the project that can be changed.
    def Update(name, ptype, description):
        self.name = name
        self.type = ptype
        self.description = description

#Class to use for individual profiles. Takes the user's id (UIN), first name, last name, persona (student or professor),
#email, primary contact, a list of associated interests, and a list of associated projects
class Profile:
    def __init__(self, uin, fname, lname, persona, email, prcontact, interests, projects):
        self.id = uin
        self.fname = fname
        self.lname = lname
        self.persona = persona
        self.email = email
        self.prcontact = prcontact
        self.interests = interests
        self.projects = projects

    def Update(fname, lname, persona, email, prcontact, interests):
        self.fname = fname
        self.lname = lname
        self.persona = persona
        self.email = email
        self.prcontact = prcontact
        self.interests = interests

    #Method to create a project associated with a profile. Allows filling in required info (like poster's name)
    #through the Profile's stored info.
    def CreateProject(projname, projtype, description):
        newProject = Project(self.fname, self.lname, projname, projtype, description)

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
    return home()

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
