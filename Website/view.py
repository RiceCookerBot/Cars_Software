from flask import Blueprint, render_template,request,url_for,redirect, session
from Website.models import Cars
from .forms import carSearchForm,registerCarForm,editCarForm
from sqlalchemy.exc import IntegrityError 
from wtforms.fields import Label
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from  .models import Cars


view = Blueprint('view',__name__)

#Lag en error Side
#Lag service Side
#Lag en registrer order side
#Lag en manage order side
#Lag flash warings i base.html
#brukere brude se ordere som de har kontroll av


#Links to other sites
@view.route('/')
@login_required
def home():
    return render_template("home.html")

@view.route('/biler',methods=['GET','POST'])
@login_required
def biler():
    form = carSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        reg = form.registration.data
        return redirect(url_for("view.bilerSearch",reg=reg), code=307)
    else:
        return render_template("biler.html",form=form,Cars=Cars)

#Åpner opp for en IDOR vulnerabilty, forgrunn av dårlig auth av request
#See denne artikkelen for mere informasjon: https://portswigger.net/web-security/access-control/idor
@view.route('/bilerSøk/<reg>', methods=['POST', 'GET'])
@login_required
def bilerSearch(reg):
    form = carSearchForm()

    # Filter query by variable
    cars = Cars.query.all()

    carRow = None
    for car in cars:
        if car.registration == reg:
            carRow = car
            break  # Stop searching once found

    if request.method == 'POST' and form.validate_on_submit():
        new_reg = form.registration.data
        return redirect(url_for('view.bilerSearch', reg=new_reg))

    # Endre til en flash
    if carRow is None:
        return render_template("bil-SøkError.html", reg=reg, form=form)

    return render_template('bil-Søk.html', form=form, car=carRow, reg=reg)
    
@view.route('/register-bil', methods=['GET','POST'])
@login_required
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
                return redirect(url_for("view.biler"))
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
@login_required
def delBil(reg):
    Cars.query.filter_by(registration=reg).delete()
    db.session.commit()
    return redirect(url_for("view.biler"))

@view.route('/edit-car/<reg>',methods=['GET','POST'])
@login_required
def editCar(reg):

    form = editCarForm()
    carsRow = Cars.query.get(reg)
    form.price.default = carsRow.price
    form.available.default = carsRow.available
    form.sold.default = carsRow.sold
    form.owner.default = carsRow.owner

    form.submit.label = Label(field_id='name',text='updater verdier')
    
    if request.method == 'POST':
        carsRow.price = form.price.data
        carsRow.available = form.available.data
        carsRow.sold = form.sold.data
        carsRow.owner = form.owner.data

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'error somthing went wrong'
        
        return redirect(url_for('view.biler'))
    else:
        form.process()
        return render_template('edit-car.html',form=form,reg=reg,car=carsRow)

@view.route('/service')
def service():
    return render_template("service.html")

@view.route('/order')
def order():
    return 'order'

@view.route('/test')
def test():
    cars = Cars.query.all()
    carRow = None
    for car in cars:
        if car.registration == 'AS45901':
            carRow = car
    
    print(carRow)
    return 'sex?'