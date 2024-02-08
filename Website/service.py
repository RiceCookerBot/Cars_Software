from flask import Blueprint, render_template,request,url_for,redirect, session
from .forms import loginForm, newUserForm
from sqlalchemy.exc import IntegrityError 

from flask_login import login_user, login_required, logout_user, current_user

from . import db
from  .models import Users


service = Blueprint('service',__name__)

@service.route('/service-page')
@login_required
def servicePage():
    return 'yea'

@service.route('/reg-order',methods=['GET','POST'])
@login_required
def regOrder():
    return 'order'