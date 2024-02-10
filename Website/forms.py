#Forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sqlalchemy import Integer
from wtforms.validators import InputRequired, Length,EqualTo,ValidationError,DataRequired
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, SubmitField, PasswordField, SelectField,DateField)
from .models import Cars, Service

class carSearchForm(FlaskForm):
    registration = StringField('Skriv registrasjonsnummer her',validators=[InputRequired(), Length(min=7, max=10)])
    submit = SubmitField('Søk')

class registerCarForm(FlaskForm):
    registration = StringField('Registrasjons nummer', validators=[InputRequired(),Length(min=7, max=10)])
    brand = StringField('Bil Merke', validators=[InputRequired()])
    model = StringField('Bil model', validators=[InputRequired()])
    color = StringField('Bil Farge', validators=[InputRequired()])
    price = IntegerField('Pris i kr', validators=[InputRequired()])
    available = BooleanField('tilgjenglig', default=True)
    sold = BooleanField('Solgt', default=False)
    owner = StringField('Eieren av Bil', default='Cars Software', validators=[InputRequired()])
    submit = SubmitField('Registrer Ny-Bil')

class editCarForm(FlaskForm):
    price = IntegerField('Pris i kr', validators=[InputRequired()])
    available = BooleanField('tilgjenglig', default=True)
    sold = BooleanField('Solgt', default=False)
    owner = StringField('Eieren av Bil', default='Cars Software', validators=[InputRequired()])
    submit = SubmitField('Registrer Ny-Bil')

class loginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[InputRequired()])
    password = PasswordField('Passord', validators=[InputRequired()])
    remember = BooleanField('Husk meg',default=False)
    submit = SubmitField('Login')

class newUserForm(FlaskForm):
    username = StringField('Brukernavn', validators=[InputRequired()])
    name = StringField('navn',validators=[InputRequired()])
    phoneNumber = StringField('Telefonnumber', validators=[InputRequired()])
    password = PasswordField('Passord', validators=[InputRequired()])
    submit = SubmitField('Registrer ny bruker')

class orderForm(FlaskForm):
    reg = SelectField('Registrasjons nummer', validators=[InputRequired()])
    customerName = StringField('Kunde navn', validators=[InputRequired()])
    customerPhone = StringField('Kunde tlf', validators=[InputRequired()])
    description = TextAreaField('beskrivelse av problem', validators=[InputRequired()])
    submit = SubmitField('Send')

class confirmOrderForm(FlaskForm):
    mecanic = StringField('Mekaniker navn', validators=[InputRequired()])
    serviceDate = DateField('Service dato')
    submit = SubmitField('Bekreft order')