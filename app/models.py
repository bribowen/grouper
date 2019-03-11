from app import db

#Dim_Project
class Project(db.Model):
    Project_ID = db.Column(db.Integer, primary_key=True)
    Original_Poster = db.Column(db.Integer, index=True)
    Project_Name = db.Column(db.String(120))
    Project_Type = db.Column(db.String(120))
    Project_Description = db.Column(db.String(500))

    def __repr__(self):
    	return '<Project {}'.format(self.Project_Description)

#Dim_Profile
class Profile(db.Model):
    uin = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    First_Name = db.Column(db.String(120))
    Last_Name = db.Column(db.String(120))
    User_Persona_Type = db.Column(db.String(60))
    Primary_Contact = db.Column(db.String(60))

    def __repr__(self):
    	return '<User {}>'.format(self.First_Name)

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
	id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.uin'), primary_key=True)
	role = db.Column(db.String(60))

#Fact_Skill
class UserSkills(db.Model):
	id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('user.uin'), primary_key=True)

#Fact_Interest
class UserInterest(db.Model):
	id = db.Column(db.Integer, db.ForeignKey('interest.id'), primary_key=True)
	uin = db.Column(db.Integer, db.ForeignKey('user.uin'), primary_key=True)

"""
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
"""
