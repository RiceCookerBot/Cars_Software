#Forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sqlalchemy import Integer
from wtforms.validators import InputRequired, Length,EqualTo,ValidationError,DataRequired
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, SubmitField, PasswordField, SelectField)

from .models import Cars, Service

class carForm(FlaskForm):
    registration = StringField('Skriv restrasjonsnummer her',validators=[InputRequired(), Length(min=0, max=6)])
    submit = SubmitField('Søk')

class loginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[InputRequired()])
    password = PasswordField('Passord', validators=[InputRequired()])
    submit = SubmitField('Login')

class userForm(FlaskForm):
    username = StringField('Brukernavn', validators=[InputRequired()])
    epost = StringField('e-post', validators=[InputRequired()])
    navn = StringField('navn',validators=[InputRequired()])
    etternavn = StringField('etternavn', validators=[InputRequired()])
    password = StringField('Passord', validators=[InputRequired()])
    submit = SubmitField('Login')

class orderForm(FlaskForm):
    serviceType = SelectField('Service', choices=[('Bil reparasjon','kontroll','problem søking')])
    clientName = StringField('Kunde Navn', validators=[InputRequired()])
    telephoneNumber = StringField('Kunde Telefon nummer', validators=[InputRequired()])
    description = StringField('Beskrivelse av service', validators=[InputRequired()])
    description = StringField('Beskrivelse av service', validators=[InputRequired()])
    submit = SubmitField('Send')