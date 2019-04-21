#!/usr/bin/env python
# File for creating the various classes/database models for adding and storing to the database.

# Importing of required libraries.
from app import db
from app import login
from flask_login import UserMixin
from datetime import datetime

# Class for creating the Project table in the database. Contains a single foreign key that references the UIN of the poster.
# Includes 2 functions. One determines how to return database queries made through Python. The second returns a Profile object provided the user's UIN.
class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    original_poster = db.Column(db.Integer, db.ForeignKey('profile.uin'), index=True)
    project_name = db.Column(db.String(120))
    project_type = db.Column(db.String(120))
    project_description = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
    	return '<Project {}'.format(self.project_description)
    
    def get_poster(self, original_poster):
        return Profile.query.filter_by(uin=original_poster).first_or_404()

# Class for creating the Profile table in the database. Includes 3 functions. __repr__ determines how to return database queries made through
# Python. set_password sets the password for the user. check_password makes sure the provided password equals the password stored within the class.
# get_id returns the UIN of the object.
class Profile(UserMixin, db.Model):
    uin = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    user_persona_type = db.Column(db.String(60))
    primary_contact = db.Column(db.String(60))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
    	return '<User {}>'.format(self.first_name)
    
    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def get_id(self):
        return (self.uin)

# Class for creating the Interest table in the database.
class Interest(db.Model):
    interest_id = db.Column(db.Integer, primary_key=True)
    interest_name = db.Column(db.String(120), unique=True)

# Class for creating the Skill table in the database.
class Skill(db.Model):
	skill_id = db.Column(db.Integer, primary_key=True)
	skill_name = db.Column(db.String(60), unique=True)

# Class for creating the Participation table in the database. This is an associative entity and contains Foreign Keys as its primary keys.
class Participation(db.Model):
	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)
	role = db.Column(db.String(60))

# Class for creating the Profile_Skill table in the database. This is an associative entity and contains Foreign Keys as its primary keys.
class ProfileSkill(db.Model):
	skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)

# Class for creating the Profile_Interest table in the database. This is an associative entity and contains Foreign Keys as its primary keys.
class ProfileInterest(db.Model):
	interest_id = db.Column(db.Integer, db.ForeignKey('interest.interest_id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)

# Class for creating the Project_Request table in the database. This is an associative entity and contains Foreign Keys as its primary keys.
# Includes 2 functions. get_requester returns the Profile that requested to be added. get_project_owner returns the Profile that owns the project.
class ProjectRequest(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
    uin = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)
    requester_fname = db.Column(db.String(60))
    requester_lname = db.Column(db.String(60))

    def get_requester(uin):
        return Profile.query.filter_by(uin=uin).first_or_404()
    
    def get_project_owner():
        return Profile.query.filter_by(uin=Project.query.filter_by(project_id=project_id).first().original_poster).first_or_404()

# Quick function for loading the user's info when logging in.
@login.user_loader
def load_user(uin):
    return Profile.query.get(int(uin))