from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Profile

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    uin = IntegerField('UIN', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    persona = StringField('Persona Type', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), 
    EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = Profile.query.filter_by(email_address=email.data).first()
        if user is not None:
            raise ValidationError('A profile with that email address is already registered.')
    
    def validat_uin(self, uin):
        user = Profile.query.filter_by(uin=uin.data).first()
        if user is not None:
            raise ValidationError('A profile with that UIN is already registered.')
