#!/usr/bin/env python
import os
from flask import flash, request, redirect, render_template, request, session, url_for, json
from flask_login import current_user, login_user, logout_user, login_manager, login_required
from app import app, db
from app.forms import ProjectForm, LoginForm, RegistrationForm, EditProfileForm
from app.models import Profile, Project
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(original_poster=current_user.uin, project_name=form.project_name.data, project_description=form.project_description.data,
            project_type=form.project_type.data)
        db.session.add(project)
        db.session.commit()
        flash('Your project is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    projects = Project.query.paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('index', page=projects.prev_num) if projects.has_prev else None
    return render_template('index.html', title='Home', form=form, projects=projects.items, next_url=next_url,
    prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('explore', page=projects.prev_num) if projects.has_prev else None
    return render_template('index.html', title='Explore', projects=projects.items, next_url=next_url,
    prev_url=prev_url)

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
def register():
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

@app.route('/user/<uin>')
@login_required
def user(uin):
    user = Profile.query.filter_by(uin=uin).first_or_404()
    page = request.args.get('page', 1, type=int)
    projects = Project.query.filter_by(original_poster=user.uin).order_by(Project.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('explore', page=projects.prev_num) if projects.has_prev else None
    return render_template('user.html', user=user, projects=projects.items,
    next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email_address = form.email.data
        current_user.first_name = form.fname.data
        current_user.last_name = form.lname.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email_address
        form.fname.data = current_user.first_name
        form.lname.data = current_user.last_name
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()