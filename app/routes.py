#!/usr/bin/env python
import os
from flask import flash, request, redirect, render_template, request, session, url_for, json
from flask_login import current_user, login_user, logout_user, login_manager, login_required
from app import app, db
from app.forms import ProjectForm, LoginForm, RegistrationForm, EditProfileForm
from app.models import Profile, Project, ProfileSkill, ProfileInterest, Skill, Interest
from werkzeug.urls import url_parse
from datetime import datetime
import MySQLdb

def get_cursor():
    connection = MySQLdb.connect(host="localhost", user="grouper", passwd="Grouper!1", db="grouper")
    return connection.cursor()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ProjectForm()
    if request.method == 'POST' and form.validate_on_submit():
        project = Project(original_poster=current_user.uin, project_name=form.project_name.data, project_description=form.project_description.data,
            project_type=form.project_type.data, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #print(project.project_name)
        db.session.add(project)
        db.session.commit()
        flash('Your project is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.timestamp.desc()).paginate(
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
        
        #Checking on interests
        interests = submit_interest(form)
        for interest in interests:
            db.session.add(interest)

        #Checking on skills
        skills = submit_skill(form)
        for skill in skills:
            db.session.add(skill)
        
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
        current_user.user_persona_type = form.persona.data
        current_user.about_me = form.about_me.data
        #Checking on interests
        interests, rem_interests = submit_interest(form)
        for interest in interests:
            db.session.add(interest)
        for interest in rem_interests:
            db.session.delete(interest)

        #Checking on skills
        skills, rem_skills = submit_skill(form)
        for skill in skills:
            db.session.add(skill)
        for skill in rem_skills:
            db.session.delete(skill)
            
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', uin=current_user.uin))
    
    elif request.method == 'GET':
        form = get_skills(form)
        form = get_interests(form)
        form.email.data = current_user.email_address
        form.fname.data = current_user.first_name
        form.lname.data = current_user.last_name
        form.persona.data = current_user.user_persona_type
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def submit_interest(form):
    interests = []
    rem_interests = []
    if form.marketing.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.marketing.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Marketing"[0].interest_id), uin=current_user.uin)
            rem_interests.append(interest).first()
    if form.art.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.art.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, 
                uin=current_user.uin).first()
            rem_interests.append(interest)
    if form.tech.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.tech.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, 
                uin=current_user.uin).first()
            rem_interests.append(interest)
    if form.event.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.event.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, 
                uin=current_user.uin).first()
            rem_interests.append(interest)
    if form.finance.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.finance.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, 
                uin=current_user.uin).first()
            rem_interests.append(interest)
    if form.healthcare.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.healthcare.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, 
                uin=current_user.uin).first()
            rem_interests.append(interest)
    if form.science.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.science.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, 
                uin=current_user.uin).first()
            rem_interests.append(interest)
    if form.affairs.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, uin=current_user.uin).count() == 0):
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, 
                uin=current_user.uin)
            interests.append(interest)
    elif not form.affairs.data:
        if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, uin=current_user.uin).count() > 0):
            interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, 
                uin=current_user.uin).first()
            rem_interests.append(interest)
    
    return interests, rem_interests

def submit_skill(form):
    skills = []
    rem_skills = []

    if form.app.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id, uin=current_user.uin).count() == 0):
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id,
                uin=current_user.uin)
            skills.append(skill)
    elif not form.app.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id, uin=current_user.uin).count() > 0):
            skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id, 
                uin=current_user.uin).first()
            rem_skills.append(skill)
    if form.datan.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, uin=current_user.uin).count() == 0):
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, 
                uin=current_user.uin)
            skills.append(skill)
    elif not form.datan.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, uin=current_user.uin).count() > 0):
            skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, 
                uin=current_user.uin).first()
            rem_skills.append(skill)
    if form.database.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, uin=current_user.uin).count() == 0):
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, 
                uin=current_user.uin)
            skills.append(skill)
    elif not form.database.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, uin=current_user.uin).count() > 0):
            skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, 
                uin=current_user.uin).first()
            rem_skills.append(skill)
    if form.document.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, uin=current_user.uin).count() == 0):
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, 
                uin=current_user.uin)
            skills.append(skill)
    elif not form.document.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, uin=current_user.uin).count() > 0):
            skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, 
                uin=current_user.uin).first()
            rem_skills.append(skill)
    if form.presentation.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, uin=current_user.uin).count() == 0):
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, 
                uin=current_user.uin)
            skills.append(skill)
    elif not form.presentation.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, uin=current_user.uin).count() > 0):
            skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, 
                uin=current_user.uin).first()
            rem_skills.append(skill)
    if form.web.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, uin=current_user.uin).count() == 0):
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, 
                uin=current_user.uin)
            skills.append(skill)
    elif not form.web.data:
        if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, uin=current_user.uin).count() > 0):
            skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, 
                uin=current_user.uin).first()
            rem_skills.append(skill)
    return skills, rem_skills

def get_skills(form):
    if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id, uin=current_user.uin).count() > 0):
        form.app.data = True

    if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, uin=current_user.uin).count() > 0):
        form.datan.data = True

    if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, uin=current_user.uin).count() > 0):
        form.database.data = True

    if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, uin=current_user.uin).count() > 0):
        form.document.data = True

    if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, uin=current_user.uin).count() > 0):
        form.presentation.data = True

    if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, uin=current_user.uin).count() > 0):
        form.web.data = True
    
    return form

def get_interests(form):

    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, uin=current_user.uin).count() > 0):
        form.marketing.data = True

    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, uin=current_user.uin).count() > 0):
        form.art.data = True
    
    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, uin=current_user.uin).count() > 0):
        form.tech.data = True

    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, uin=current_user.uin).count() > 0):
        form.event.data = True

    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, uin=current_user.uin).count() > 0):
        form.finance.data = True

    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, uin=current_user.uin).count() > 0):
        form.healthcare.data = True

    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, uin=current_user.uin).count() > 0):
        form.science.data = True

    if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, uin=current_user.uin).count() > 0):
        form.affairs.data = True

    return form