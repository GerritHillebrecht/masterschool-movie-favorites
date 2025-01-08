from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, TimeField, DateField
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField("Firstname", validators=[DataRequired()])
    lastname = StringField("Lastname", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class MovieForm(FlaskForm):
    name = StringField("Movie Title", validators=[DataRequired()])
    poster = StringField("Poster", validators=[DataRequired()])
    watch_time = TimeField("Time", validators=[DataRequired()])
    watch_date = DateField("Date", validators=[DataRequired()], default=datetime.today)
    plot = TextAreaField("Movie Plot", validators=[DataRequired()])
