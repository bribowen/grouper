#!/usr/bin/env python
#This file describes specific configurations for the flask environment.

#Imports the os library then describes the path to the base directory of the application.
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Creates a class to describe the configurations for the rest of the file. Most are pulled in the __init__.py file.
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://Grouper:Grouper!1@grouper.czauevigug7j.us-east-2.rds.amazonaws.com/grouper'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
