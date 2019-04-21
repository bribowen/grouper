#!/usr/bin/env python
# This file creates the various forms rendered in the html files. Allows for building dynamic web pages
# and utilizing previously created form templates.

# Importing of various libraries/files needed. WTForms is the main library used here, along with flaskwtf which
# integrates WTForms more seamlessly into Flask environments.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import Profile

# Login form that displays the various pieces for logging in as displayed on the login.html page.
# Data validation is included for the email and password fields ensuring the
# user does actually input something. WTForms includes a password-specific field for rendering a form for password input.
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Registration form. Displays the various fields required for the registration.html page. The various Boolean fields are for user interests/skills.
# A bit more complicated, as various types of fields are included such as drop down menus and check boxes.
# Includes a pair of functions to validate that the email and UIN provided have not already been claimed.
class RegistrationForm(FlaskForm):
    # List of tuples used for creating the dropdown menu for the persona field.
    persona_choices = [('Student', 'Student'), ('Faculty', 'Faculty')]

    uin = IntegerField('UIN', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    persona = SelectField('Persona Type', choices=persona_choices, validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    marketing = BooleanField('Marketing')
    art = BooleanField('Art/Media/Communication')
    tech = BooleanField('Emerging Technology')
    event = BooleanField('Event Management')
    finance = BooleanField('Finance')
    healthcare = BooleanField('Healthcare')
    science = BooleanField('Science')
    affairs = BooleanField('Student Affairs')
    app = BooleanField('App Programming')
    datan = BooleanField('Data Analysis')
    database = BooleanField('Database Design')
    document = BooleanField('Documentation')
    presentation = BooleanField('Presentation')
    web = BooleanField('Web Development')
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = Profile.query.filter_by(email_address=email.data).first()
        if user is not None:
            raise ValidationError('A profile with that email address is already registered.')
    
    def validate_uin(self, uin):
        user = Profile.query.filter_by(uin=uin.data).first()
        if user is not None:
            raise ValidationError('A profile with that UIN is already registered.')

# Form to allow users to edit their profile from the user.html page. Displays all the information inputted besides password and
# UIN.
class EditProfileForm(FlaskForm):
    # List of tuples used for creating the dropdown menu for the persona field.
    choices = [('Student', 'Student'), ('Faculty', 'Faculty')]

    email = StringField('Email', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    persona = SelectField('Persona Type', choices=choices, validators=[DataRequired()])
    marketing = BooleanField('Marketing')
    art = BooleanField('Art/Media/Communication')
    tech = BooleanField('Emerging Technology')
    event = BooleanField('Event Management')
    finance = BooleanField('Finance')
    healthcare = BooleanField('Healthcare')
    science = BooleanField('Science')
    affairs = BooleanField('Student Affairs')
    app = BooleanField('App Programming')
    datan = BooleanField('Data Analysis')
    database = BooleanField('Database Design')
    document = BooleanField('Documentation')
    presentation = BooleanField('Presentation')
    web = BooleanField('Web Development')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

# Form to create projects, displayed on the index.html page.
class ProjectForm(FlaskForm):
    choices=[('Application Development', 'Application Development'),
    ('Online Retail', 'Online Retail'),
    ('Database Management', 'Database Management'),
    ('Machine Learning', 'Machine Learning')]

    project_name = StringField('Project Name', validators=[DataRequired()])
    project_type = SelectField('Project Type', choices=choices, validators=[DataRequired()])
    project_description = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

# Form that allows users to request to join a project as displayed on the project.html page. Only requires a single button. 
class JoinForm(FlaskForm):
    join = SubmitField('Request to join this project')

# Form that allows a project owner to accept or deny a user's request to join a project, as displayed on the project.html page.
class RequestForm(FlaskForm):
    choices=[('Accept', 'Accept'), ('Deny', 'Deny')]

    request1 = RadioField('', choices=choices)
    request2 = RadioField('', choices=choices)
    request3 = RadioField('', choices=choices)
    request4 = RadioField('', choices=choices)
    request5 = RadioField('', choices=choices)

    accept1 = BooleanField('Accept')
    deny1 = BooleanField('Deny')
    accept2 = BooleanField('Accept')
    deny2 = BooleanField('Deny')
    accept3 = BooleanField('Accept')
    deny3 = BooleanField('Deny')
    accept4 = BooleanField('Accept')
    deny4 = BooleanField('Deny')
    accept5 = BooleanField('Accept')
    deny5 = BooleanField('Deny')
    submit = SubmitField('Submit')

class FilterForm(FlaskForm):
    choices=[('Application Development', 'Application Development'),
    ('Online Retail', 'Online Retail'),
    ('Database Management', 'Database Management'),
    ('Machine Learning', 'Machine Learning')]

    project_type = SelectField('Project Type', choices=choices)
    filter = SubmitField('Filter Projects')

class DeleteForm(FlaskForm):
    delete = SubmitField('Delete Project')