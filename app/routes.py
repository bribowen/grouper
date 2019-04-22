#!/usr/bin/env python
# This file handles all the routing of the application. Also includes a few functions necessary for allowing the routing to work properly.

# Importing of various libraries necessary.
import os
# The flask library contains several of the functions called throughout the file. Many required for basic function.
from flask import flash, request, redirect, render_template, request, session, url_for, json
from flask_login import current_user, login_user, logout_user, login_manager, login_required
from werkzeug.urls import url_parse
from datetime import datetime
import MySQLdb

# Importing of classes from the application.
from app import app, db
from app.forms import JoinForm, ProjectForm, LoginForm, RegistrationForm, EditProfileForm, RequestForm, FilterForm, DeleteForm
from app.models import Participation, Profile, Project, ProfileSkill, ProfileInterest, Skill, Interest, ProjectRequest

# Provides a cursor for use with direct database queries.
def get_cursor():
    connection = MySQLdb.connect(host="localhost", user="grouper", passwd="Grouper!1", db="grouper")
    return connection.cursor()

# @app.route tells the server what to append to the URL for the page. Allows users to browse directly via the URL and also useful
# for easy redirecting.
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# Calling the login_required function ensures a user can't browse to the page without logging in.
@login_required
# Creates the base index page.
def index():
    # Creates a variable to store the forms used for the page. In this case, the submission would be a project, so the Project Form is rendered.
    projectform = ProjectForm()
    # Determines whether something was submitted.
    if request.method == 'POST' and projectform.validate_on_submit():
        # Creates a Project object based on submitted data from the .html file.
        project = Project(original_poster=current_user.uin, project_name=projectform.project_name.data, project_description=projectform.project_description.data,
            project_type=projectform.project_type.data, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # db.session.add() adds the object to the database session. Multiple objects for multiple tables can be added before they are commited to the
        # database through db.session.commit()
        db.session.add(project)
        db.session.commit()
        # Flashes a message on successful submission of the project.
        flash('Your project is now live!')
        # Redirects the user to the index page, which in this case is the same page. Includes the flashed message.
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)

    # Creates a list for all the projects, then uses a for loop to retrieve them.
    projects = []
    for project in Project.query.order_by(Project.timestamp.desc()):
        projects.append(project)

    # Creates a set of lists for separating the projects into four groups.
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    # Separates the projects equally into the 4 lists.
    for project in projects:
        if (projects.index(project) % 4) == 0:
            list1.append(project)
        elif (projects.index(project) % 4) == 1:
            list2.append(project)
        elif (projects.index(project) % 4) == 2:
            list3.append(project)
        elif (projects.index(project) % 4) == 3:
            list4.append(project)
    # Renders the index.html page. render_template always takes a set of variables (name of the .html file
    # and a page file) along with any variables called from Jinja2 on the .html page.
    # In this case, the form, list of projects, and 4 separate lists are all passed to the page.
    return render_template('index.html', title='Home', projectform=projectform,
     projects=projects, list1=list1, list2=list2, list3=list3, list4=list4) 

# Renders the page for an individual project. The project's ID is passed and used as the second part of the URL, allowing for
# dynamic creation of web pages instead of a file being created for each individual project.
@app.route('/project/<project_id>', methods=['GET', 'POST'])
@login_required
# Functions takes the project_id as a variable. Should be passed automatically through a redirect.
def project(project_id):
    # Grabs the project as a variable. Then creates two lists to hold the current members of the project and any requests to join the project.
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    members = []
    requests = []
    joinform = JoinForm()
    deleteform = DeleteForm()
    requestform = RequestForm()
    # Loop to grab all members of the project and add them to the members list.
    for result in Participation.query.filter_by(project_id=project.project_id):
        member = Profile.query.filter_by(uin=result.member_id).first()
        members.append(member)
    
    # Checks to see if the user viewing the project is the project owner. If not, it renders the
    # Join form to allow the user to request to join the project.
    if current_user != project.get_poster(project.original_poster):
        joinform = JoinForm()
        if form.validate_on_submit():
            # Checks to see if there is space on the project and the user isn't already listed on it.
            if check_number_users(project) and check_user(project, current_user):
                proj_request = ProjectRequest(project_id=project.project_id, uin=current_user.uin,
                 requester_fname=current_user.first_name, requester_lname=current_user.last_name)
                db.session.add(proj_request)
                db.session.commit()
                flash("The project owner will be notified of your request.")
            # Flashes a message if there are already 5 people on the project (the maximum).
            elif not check_number_users(project):
                flash('There are already 5 people on this project.')
                return redirect(url_for('project', project_id=project.project_id))
            # Flashes a message if the user is already on the project.
            elif not check_user(project, current_user):
                flash("You're already on this project.")
                return redirect(url_for('project', project_id=project.project_id))
    # If the user is the project owner, it renders the Request form, allowing the user to decide whether they want to accept/deny
    # any project join requests.
    else:
        deleteform = DeleteForm()
        requestform = RequestForm()
        # Invokes the get_requests method to retrieve all requests for the project.
        requests = get_requests(current_user, project)
        if requestform.validate_on_submit():
            # Series of conditionals that checks to see which accept/deny boxes contain data and to act appropriately.
            # As an example, this first one will check if the accept box contained data. If so, it adds the user who created the requests
            # to the project. Otherwise, it deletes the request.
            if requestform.accept1.data and requests[0]:
                proj_req = requests[0]
                participation = Participation(project_id=project.project_id, member_id=proj_req.uin, role="Member")
                db.session.add(participation)
                db.session.delete(proj_req)
            elif requestform.deny1.data and requests[0]:
                db.session.delete(requests[0])
            if requestform.accept2.data and requests[1]:
                proj_req = requests[1]
                participation = Participation(project_id=project.project_id, member_id=proj_req.uin, role="Member")
                db.session.add(participation)
                db.session.delete(proj_req)
            elif requestform.deny1.data and requests[1]:
                db.session.delete(requests[1])
            if requestform.accept3.data and requests[2]:
                proj_req = requests[2]
                participation = Participation(project_id=project.project_id, member_id=proj_req.uin, role="Member")
                db.session.add(participation)
                db.session.delete(proj_req)
            elif requestform.deny1.data and requests[2]:
                db.session.delete(requests[2])
            if requestform.accept4.data and requests[3]:
                proj_req = requests[3]
                participation = Participation(project_id=project.project_id, member_id=proj_req.uin, role="Member")
                db.session.add(participation)
                db.session.delete(proj_req)
            elif requestform.deny1.data and requests[3]:
                db.session.delete(requests[3])
            if requestform.accept5.data and requests[4]:
                proj_req = requests[4]
                participation = Participation(project_id=project.project_id, member_id=proj_req.uin, role="Member")
                db.session.add(participation)
                db.session.delete(proj_req)
            elif requestform.deny1.data and requests[4]:
                db.session.delete(requests[4])
            # With all changes made, it commits the changes to the database, flashes a message to the user, and returns a redirect to the 
            # URL of the same project page (refreshes, essentially
            db.session.commit()
            flash("Changes successfully made.")
            return redirect(url_for('project', project_id=project.project_id))
        # Checks to see if the owner wants to delete the project. If so, it removes the participants from the project then deletes the project.
        if deleteform.validate_on_submit():
            participations = Participation.query.filter_by(project_id=project.project_id).all()
            for participation in participations:
                db.session.delete(participation)
            db.session.commit()
            db.session.delete(project)
            db.session.commit()
            flash("Project deleted.")
            return redirect(url_for('index'))
    # Renders the project page with the appropriate form, list of members on the project, the project itself, and requests to join the project.
    return render_template('project.html', title='Project', requestform=requestform, joinform=joinform, deleteform=deleteform, members=members, project=project, requests=requests)

# Renders the explore page. Requires login.
@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    # Creates the form for filtering.
	filterform = FilterForm()
	page = request.args.get('page', 1, type=int)
    # Gets the list of projects.
	projects = Project.query.order_by(Project.timestamp.desc()).all()
    # Checks if the form has been submitted and, if so, gets the list of projects associated with the filtered type.
	if filterform.validate_on_submit():
		filter = filterform.project_type.data
		projects = Project.query.filter_by(project_type=filter).all()
    # Creates a set of lists for separating the projects into four groups.
	list1 = []
	list2 = []
	list3 = []
	list4 = []
    # Separates the projects equally into the 4 lists.
	for project in projects:
		if (projects.index(project) % 4) == 0:
			list1.append(project)
		elif (projects.index(project) % 4) == 1:
			list2.append(project)
		elif (projects.index(project) % 4) == 2:
			list3.append(project)
		elif (projects.index(project) % 4) == 3:
			list4.append(project)
    # Renders index.html. Does so because of the small difference between the index and explore pages. Renders the page without the project submission form.
	return render_template('index.html', title='Explore', projects=projects, filterform=filterform, list1=list1, list2=list2, list3=list3, list4=list4)

# Route for logging in. All pages redirect here if the user is not logged in.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Checks if the user is authenticated. If so, redirects to the index page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Creates the login form for submission.
    form = LoginForm()
    if form.validate_on_submit():
        # Checks if the user exists in the database. If not, flashes a relevant message and returns the login page.
        user = Profile.query.filter_by(email_address=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Logs the user in and redirects to the index page.
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

# Route for the register page. The login page links here.
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Checks if the user is authenticated. If so, redirects to the index page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Creates the registration form for submission.
    form = RegistrationForm()
    if form.validate_on_submit():
        # Checks if UIN is an integer. If not, returns an error.
        if not type(form.uin.data) == int:
            flash('UIN must be an integer.')
            return redirect(url_for('register'))
        # Creates the user object according to the inputted information.
        user = Profile(uin=form.uin.data, email_address=form.email.data, first_name=form.fname.data,
        last_name=form.lname.data, user_persona_type=form.persona.data, primary_contact=form.phone.data)
        user.set_password(form.password.data)
        # 3 data validation chceks. One to ensure the UIN is not already in use, one to ensure the email is not already in use,
        # and one to ensure the UIN is not too long.
        if user.check_uin(user.uin):
            flash('There is already a user registered with that UIN.')
            return redirect(url_for('register'))
        elif user.check_email(user.email):
            flash('There is already a user registered with that email.')
            return redirect(url_for('register'))
        if user.check_uin_length(user.uin):
            flash('Please enter a UIN of 11 digits or less.')
            return redirect(url_for('register'))
        # User is added to the database.
        db.session.add(user)
        # Checking on submitted interests and adding them to the DB as necessary.
        interests, rem_interests = submit_interest(form)
        for interest in interests:
            db.session.add(interest)
        for interest in rem_interests:
            db.session.delete(interest)

        # Checking on submitted interests and adding them to the DB as necessary.
        skills, rem_skills = submit_skill(form)
        for skill in skills:
            db.session.add(skill)
        for skill in rem_skills:
            db.session.delete(skill)
        
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Route to log the user out.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route to render the user's profile page. Requires a UIN as the second part of the URL for dynamically creating the page.
@app.route('/user/<uin>')
@login_required
def user(uin):
    # Gets the user as an object according to submitted UIN. Then gets all the user's skills and interests.
    user = Profile.query.filter_by(uin=uin).first_or_404()
    profileskills = ProfileSkill.query.filter_by(uin=uin).all()
    profileinterests = ProfileInterest.query.filter_by(uin=uin).all()
    interests = []
    skills = []
    for result in profileinterests:
        interest = Interest.query.filter_by(interest_id=result.interest_id).first()
        interests.append(interest)
    for result in profileskills:
        skill = Skill.query.filter_by(skill_id=result.skill_id).first()
        skills.append(skill)
    page = request.args.get('page', 1, type=int)
    # Gets a list of projects created by the user.
    projects = Project.query.filter_by(original_poster=user.uin).order_by(Project.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('user.html', user=user, projects=projects.items, skills=skills,
    interests=interests, form=form)

# Route to edit the user's profile. Found on the profile page.
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Form to hold and receive data changed/added by the user.
    form = EditProfileForm()
    # If the form is submitted, it takes all the data and updates it in the database. This includes changed interests/skills.
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
    # If the HTTP sends a GET request, it returns info about the user.
    elif request.method == 'GET':
        form = get_skills(form)
        form = get_interests(form)
        form.email.data = current_user.email_address
        form.fname.data = current_user.first_name
        form.lname.data = current_user.last_name
        form.persona.data = current_user.user_persona_type
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# Used before any request by the user. Sets the current user's last seen variable in the as the current time in UTC.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# Function to check the number of users on a project and ensure it's not more than 5.
def check_number_users(project):
    return (Participation.query.filter_by(project_id=project.project_id).count() < 5)

# Function to check if the user is already on a project..
def check_user(project, user):
    return (Participation.query.filter_by(project_id=project.project_id, member_id=user.uin).count() == 0) or (ProjectRequest.query.filter_by(project_id=project_id, uin=user.uin).count() == 0)

# Function to get the requests to join a project.
def get_requests(current_user, project):
    requests = []
    for item in ProjectRequest.query.filter_by(project_id=project.project_id):
        requests.append(item)
    return requests

# Really terribly written function to get all of the interest changes submitted by a profile. Each interest is checked to see whether the user
# already had it or not. Then it checks to see if that info was changed. It creates a list to add/remove from the database and returns both as a tuple.
def submit_interest(form):
    interests = []
    rem_interests = []
    if form.marketing.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id,
                uin=form.uin.data)
            interest.append(interest)
    elif not form.marketing.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Marketing")[0].interest_id, uin=current_user.uin).first()
                rem_interests.append(interest)
    if form.art.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id,
                uin=form.uin.data)
            interests.append(interest)
    elif not form.art.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Art/Media/Communication")[0].interest_id, 
                    uin=current_user.uin).first()
                rem_interests.append(interest)
    if form.tech.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id,
                uin=form.uin.data)
            interests.append(interest)
    elif not form.tech.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Emerging Technology")[0].interest_id, 
                    uin=current_user.uin).first()
                rem_interests.append(interest)
    if form.event.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id,
                uin=form.uin.data)
            interests.append(interest)
    elif not form.event.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Event Management")[0].interest_id, 
                    uin=current_user.uin).first()
                rem_interests.append(interest)
    if form.finance.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id,
                uin=form.uin.data)
            interests.append(interest)
    elif not form.finance.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Finance")[0].interest_id, 
                    uin=current_user.uin).first()
                rem_interests.append(interest)
    if form.healthcare.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id,
                uin=form.uin.data)
            interests.append(interest)
    elif not form.healthcare.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Healthcare")[0].interest_id, 
                    uin=current_user.uin).first()
                rem_interests.append(interest)
    if form.science.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id,
                uin=form.uin.data)
            interests.append(interest)
    elif not form.science.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Science")[0].interest_id, 
                    uin=current_user.uin).first()
            rem_interests.append(interest)
    if form.affairs.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, uin=current_user.uin).count() == 0):
                interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, 
                    uin=current_user.uin)
                interests.append(interest)
        else:
            interest = ProfileInterest(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id,
                uin=form.uin.data)
            interests.append(interest)
    elif not form.affairs.data:
        if current_user.is_authenticated:
            if (ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, uin=current_user.uin).count() > 0):
                interest = ProfileInterest.query.filter_by(interest_id=Interest.query.filter_by(interest_name="Student Affairs")[0].interest_id, 
                    uin=current_user.uin).first()
                rem_interests.append(interest)
    
    return interests, rem_interests

# Same as the interest function above but with skills.
def submit_skill(form):
    skills = []
    rem_skills = []

    if form.app.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id, uin=current_user.uin).count() == 0):
                skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id,
                    uin=current_user.uin)
                skills.append(skill)
        else:
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id,
                uin=form.uin.data)
            skills.append(skill)
    elif not form.app.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id, uin=current_user.uin).count() > 0):
                skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="App Programming")[0].skill_id, 
                    uin=current_user.uin).first()
                rem_skills.append(skill)
    if form.datan.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, uin=current_user.uin).count() == 0):
                skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, 
                    uin=current_user.uin)
                skills.append(skill)
        else:
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id,
                uin=form.uin.data)
            skills.append(skill)
    elif not form.datan.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, uin=current_user.uin).count() > 0):
                skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Data Analysis")[0].skill_id, 
                    uin=current_user.uin).first()
                rem_skills.append(skill)
    if form.database.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, uin=current_user.uin).count() == 0):
                skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, 
                    uin=current_user.uin)
                skills.append(skill)
        else:
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id,
                uin=form.uin.data)
            skills.append(skill)
    elif not form.database.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, uin=current_user.uin).count() > 0):
                skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Database Design")[0].skill_id, 
                    uin=current_user.uin).first()
                rem_skills.append(skill)
    if form.document.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, uin=current_user.uin).count() == 0):
                skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, 
                    uin=current_user.uin)
                skills.append(skill)
        else:
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id,
                uin=form.uin.data)
            skills.append(skill)
    elif not form.document.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, uin=current_user.uin).count() > 0):
                skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Documentation")[0].skill_id, 
                    uin=current_user.uin).first()
                rem_skills.append(skill)
    if form.presentation.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, uin=current_user.uin).count() == 0):
                skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, 
                    uin=current_user.uin)
                skills.append(skill)
        else:
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id,
                uin=form.uin.data)
            skills.append(skill)
    elif not form.presentation.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, uin=current_user.uin).count() > 0):
                skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Presentation")[0].skill_id, 
                    uin=current_user.uin).first()
                rem_skills.append(skill)
    if form.web.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, uin=current_user.uin).count() == 0):
                skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, 
                    uin=current_user.uin)
                skills.append(skill)
        else:
            skill = ProfileSkill(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id,
                uin=form.uin.data)
            skills.append(skill)
    elif not form.web.data:
        if current_user.is_authenticated:
            if (ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, uin=current_user.uin).count() > 0):
                skill = ProfileSkill.query.filter_by(skill_id=Skill.query.filter_by(skill_name="Web Development")[0].skill_id, 
                    uin=current_user.uin).first()
                rem_skills.append(skill)
    return skills, rem_skills

# Gets a list of skills associated with the profile and fills in the related form items.
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

# Same as the skill function above but with interests.
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