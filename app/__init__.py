#!/usr/bin/env python
#This file integrates the various configurations and invokes the app.run command to start the environment.

#Importing various libraries necessary to run the environment.
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#Creates the app variable which stores the Flask environment.
app = Flask(__name__)
#Sets the configurations from the config.py file.
app.config.from_object(Config)
#Creates the SQLAlchemy database object utilizing the app.
db = SQLAlchemy(app)
#Sets up database migration tool.
migrate = Migrate(app, db)
#Creates the login manager variable.
login = LoginManager(app)
login.login_view = 'login'

#Imports the required files from the same directory.
from app import routes, models, errors

#Runs the application.
if __name__ == "__main__":
    app.run()
