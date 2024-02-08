from flask import Blueprint, render_template,request,url_for,redirect, session
from Website.models import Cars, Service
from .forms import carSearchForm,registerCarForm
from sqlalchemy.exc import IntegrityError 
import urllib.parse 

from . import db
from  .models import Cars


view = Blueprint('view',__name__)

#Lag en error Side
#Lag service Side
#Lag en registrer order side
#Lag en manage order side
#Lag en manage biler, der du kan slette biler og redigere dem
#Lag flash warings i base.html


#Links to other sites
@view.route('/')
def home():
    return render_template("home.html")

@view.route('/biler',methods=['GET','POST'])
def biler():
    form = carSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        reg = form.registration.data
        return redirect(url_for("view.bilerSearch",reg=reg), code=307)
    else:
        return render_template("biler.html",form=form,Cars=Cars)

#Åpner opp for en IDOR vulnerabilty, forgrunn av dårlig auth av request
#See denne artikkelen for mere informasjon: https://portswigger.net/web-security/access-control/idor
#Fix Bug: Cant query row with reg variable. !IMPORTANT
@view.route('/bilerSøk/<reg>',methods=['POST','GET'])
def bilerSearch(reg):
    form = carSearchForm()
    #Filter query by variable
    cars = Cars.query.all()

    carRow = None
    for car in cars:
       print(type(car.registration),type(reg))
       if car.registration == reg:
            carRow = car

    #Endre til en flash 
    if carRow == None:
        return render_template("bil-SøkError.html",reg=reg,form=form)
    
    if request.method == 'POST' and form.validate_on_submit():
        newReg = form.registration.data
        return redirect(url_for('view.bilerSearch',reg=newReg),code=302)
    else:
        return render_template('bil-Søk.html',form=form,car=carRow,reg=reg)
    
@view.route('/register-bil', methods=['GET','POST'])
def RegBil():
    form = registerCarForm()
    if request.method == 'POST' and form.validate_on_submit():
        #Form Variables
        reg = form.registration.data
        brand = form.brand.data
        model = form.model.data
        color = form.color.data
        price = form.price.data
        available = form.available.data
        sold = form.sold.data
        owner = form.owner.data

        checkReg = Cars.query.filter_by(registration=reg).first()
        if checkReg != None:
            return 'error reg already exists'
        
        car = Cars(registration=reg,brand=brand,model=model,color=color,price=price,available=available,sold=sold,owner=owner)
        if car != None:
            #Adds form data to model variable

            #Adds model data into database
            db.session.add(car)
            
            #Checks for error when commiting database changes
            #if there is. Return error page
            try:
                db.session.commit()
                return url_for("view.home")
            except IntegrityError:
                print('Somthing went wront, returning error page')
                db.session.rollback()
                #Return an error or flask-flash 
                return 'error'
        else:
            return "error"
    else:
        return render_template("reg-bil.html",form=form)
    
#Add a safe guard to deleting an object. f.exp > Flash waring
#Redirect to last visited site
@view.route('/del-bil/<reg>')
def delBil(reg):
    Cars.query.filter_by(registration=reg).delete()
    db.session.commit()
    return redirect(url_for("view.biler"))

@view.route('/edit-car/<reg>')
def editCar(reg):

    form = registerCarForm
    return 'test'

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


@view.route('/test')
def test():
    cars = Cars.query.all()
    carRow = None
    for car in cars:
        if car.registration == 'AS45901':
            carRow = car
    
    print(carRow)
    return 'sex?'