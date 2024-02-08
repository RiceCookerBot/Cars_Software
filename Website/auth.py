from flask import Blueprint, render_template,request,url_for,redirect, session
from .forms import loginForm, newUserForm
from sqlalchemy.exc import IntegrityError 

from flask_login import login_user, login_required, logout_user, current_user

from . import db
from  .models import Users

#Hashing
import hashlib


auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    form = loginForm()
    
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = Users.query.filter_by(username=username).first()
        checkUsername = Users.query.filter(Users.username == form.username.data).first()

        if checkUsername == None:
            return 'error'
        
        if compareHash(password,user.password):
            login_user(user, remember=remember)
            return redirect(url_for('view.home'))
        else:
            #Raze error with flash on login page on login failure
            return redirect(url_for('auth.login'))
    else:
        return render_template('Auth/login.html',form=form)

@auth.route('/ny-bruker',methods=['GET', 'POST'])
def newUser():
    form = newUserForm()
    if request.method == 'POST' and form.validate_on_submit():

        user = Users(username=form.username.data,name=form.name.data,phoneNumber=form.phoneNumber.data,password=hashpassword(form.password.data))

        checkUsername = Users.query.filter(Users.username == form.username.data).first()
        checkPhonenumber = Users.query.filter(Users.username == form.phoneNumber.data).first()

        if checkUsername != None:
            return 'error'
        
        if checkPhonenumber != None:
            return 'error'
        
        db.session.add(user)
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'error'
        
        return redirect(url_for("auth.login"))
        

    return render_template("Auth/newUser.html",form=form)



#redirect to login
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


#Hashing password in SHA512 and returns hash as output
def hashpassword(password):

    m = hashlib.new("SHA512")

    m.update(password.encode())
    hashedPassword = m.hexdigest()
    
    return hashedPassword

#compares inputed password value with inputed hash value.
#returns either true if password and hash are equal
#retruns false if they are not equel
def compareHash(password, hash):
    #m = hashing algorithm
    m = hashlib.new('SHA512')
    #hashes password encoded password ( utf-8 )
    m.update(password.encode())
    
    #compares hash with m.hexdigest output
    if m.hexdigest() == hash:
        print("They are the same !")
        return True

    else:
        print("There are not the same")
        return False