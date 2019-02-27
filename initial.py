#!/usr/bin/env python

import login

#Class to use for individual projects. Takes in the poster's first/last name, the project name,
#the project type (individual or for a class), and a brief description.
class Project:
    def __init__(self, posterfname, posterlname, projname, projtype, description):
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
    def __init__(self, id, fname, lname, persona, email, prcontact, interests, projects):
        self.id = id
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
        
