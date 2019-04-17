from app import db
from app import login
from flask_login import UserMixin
from datetime import datetime

#p = Project(original_poster=4, project_name="fun", project_type="fun", project_description="fun")
#Dim_Project
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
        q = db.session.query(Profile, Project).join(Project).filter(Profile.uin == original_poster)
        return q[0][0]

#u = Profile(uin='123412341', email_address='monkey@monkey.com', password='1234', first_name='lol', last_name='lol', user_persona_type='idk', primary_contact='1234123412')

#Dim_Profile
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

#Dim_Interests
class Interest(db.Model):
    interest_id = db.Column(db.Integer, primary_key=True)
    interest_name = db.Column(db.String(120), unique=True)

#Dim_Skill
class Skill(db.Model):
	skill_id = db.Column(db.Integer, primary_key=True)
	skill_name = db.Column(db.String(60), unique=True)

#Fact_Participation
class Participation(db.Model):
	project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)
	role = db.Column(db.String(60))

#Fact_Skill
class ProfileSkill(db.Model):
	skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)

#Fact_Interest
class ProfileInterest(db.Model):
	interest_id = db.Column(db.Integer, db.ForeignKey('interest.interest_id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)

class Request(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
    uin = db.Column(db.Integer, db.ForeignKey('profile.uin'), primary_key=True)
    requester_fname = db.Column(db.String(60))
    requester_lname = db.Column(db.String(60))

    def get_requester(uin):
        return Profile.query.filter_by(uin=uin).first()

@login.user_loader
def load_user(uin):
    return Profile.query.get(int(uin))