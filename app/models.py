from app import db

#Dim_Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.Integer, index=True)
    name = db.Column(db.String(120))
    ptype = db.Column(db.String(120))
    description = db.Column(db.String(500))

    def __repr__(self):
    	return '<Project {}'.format(self.description)

#Dim_Profile
class User(db.Model):
    uin = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    persona = db.Column(db.String(60))
    phone = db.Column(db.Long)

    def __repr__(self):
    	return '<User {}>'.format(self.firstName)

#Dim_Interests
class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

#Dim_Skill
class Skill(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)

#Fact_Participation
class Participation(db.Model):
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.uin'), primary_key=True)
	role = db.Column(db.String(60))

#Fact_Skill
class UserSkills(db.Model)
	id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('user.uin'), primary_key=True)

#Fact_Interest
class UserInterest(db.Model):
	id = db.Column(db.Integer, db.ForeignKey('interest.id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('user.uin'), primary_key=True)