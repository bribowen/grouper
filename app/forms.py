from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import Profile

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
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
    
    def validat_uin(self, uin):
        user = Profile.query.filter_by(uin=uin.data).first()
        if user is not None:
            raise ValidationError('A profile with that UIN is already registered.')

class EditProfileForm(FlaskForm):
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

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_type = StringField('Project Type', validators=[DataRequired()])
    project_description = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')