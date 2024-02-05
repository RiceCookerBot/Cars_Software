from flask import Blueprint, render_template,request,url_for,redirect
from Website.models import Cars, Service
from .forms import carForm


view = Blueprint('view',__name__)

#Links to other sites
@view.route('/')
def home():
    return render_template("home.html")

@view.route('/biler',methods=['GET','POST'])
def biler():
    form = carForm()
    if request.method == 'POST':

        redirect(url_for("view.biler"))
    else:
        return render_template("biler.html",form=form)

#Åpner opp for en IDOR vulnerabilty, forgrunn av dårlig auth av request
#See denne artikkelen for mere informasjon: https://portswigger.net/web-security/access-control/idor
@view.route('/biler/<id>')
def bilerSearch(id):
    return id


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