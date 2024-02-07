from flask import Blueprint, render_template,request,url_for,redirect
from Website.models import Cars, Service
from .forms import carForm

from . import db
from  .models import Cars

view = Blueprint('view',__name__)

#Lag en route som legger til nye biler inni databasen
#Skal helst gjøres innen Torsdag

#Links to other sites
@view.route('/')
def home():
    return render_template("home.html")

@view.route('/biler',methods=['GET','POST'])
def biler():
    form = carForm()
    if request.method == 'POST':
        reg = form.registration.data
        return redirect(url_for("view.bilerSearch",reg=reg))
    else:
        return render_template("biler.html",form=form)

#Åpner opp for en IDOR vulnerabilty, forgrunn av dårlig auth av request
#See denne artikkelen for mere informasjon: https://portswigger.net/web-security/access-control/idor
@view.route('/biler/<reg>')
def bilerSearch(reg):
    regExists = Cars.query.filter_by(registration=reg).scalar()
    if regExists:
        return f"reg {reg} exists"
    return f"reg there are no car with reg of {reg}"

@view.route('/service')
def service():
    return render_template("service.html")

@view.route('/order')
def order():
    return 'order'

@view.route('/login')
def login():
    return 'test'

@view.route('/new-user')
def newUser():
    return 'test'
#redirect to homepage
@view.route('/logout')
def logout():
    #Logout user
    #Create Logout function
    return redirect(url_for("view.home"))