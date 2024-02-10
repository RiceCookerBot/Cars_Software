from flask import Blueprint, render_template,request,url_for,redirect, session,flash
from .forms import orderForm, confirmOrderForm
from sqlalchemy.exc import IntegrityError 

from flask_login import login_user, login_required, logout_user, current_user

from . import db
from  .models import Order, Service,Cars

from datetime import datetime


service = Blueprint('service',__name__)

@service.route('/service-page')
@login_required
def servicePage():
    return render_template('Service/service.html',Order=Order,Service=Service)

@service.route('/ny-order',methods=['GET','POST'])
@login_required
def NyOrder():
    form = orderForm()
    form.reg.choices = [(g.registration) for g in Cars.query.order_by('registration')]

    if session['username'] == None:
        return 'error, no username in session, Logout'
    
    if request.method == 'POST' and form.validate_on_submit():
        current_usr = session['username']
        order = Order(
            registration=form.reg.data,
            employeeUsr=current_usr,
            order_date=datetime.now(),
            description=form.description.data,
            customerName=form.customerName.data,
            customerPhone=form.customerPhone.data
            )
        
        db.session.add(order)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'error'

        return redirect(url_for('service.servicePage'),code=302)
    else:
        return render_template('Service/NyOrder.html',form=form)

#confirm order take input of order id, assign mecanic on order
@service.route('bekreft-order/<orderID>', methods=['GET','POST'])
@login_required
def confirmOrder(orderID):
    form = confirmOrderForm()
    order = Order.query.filter_by(id=orderID).first()
    
    if order == None:
        return 'error, Couldn\'t get order'
    
    if request.method == 'POST' and form.validate_on_submit():
        service = Service(
            registration=order.registration,
            date=form.serviceDate.data,
            description=order.description,
            mechanic=form.mecanic.data,
            customerName=order.customerName,
            customerPhone=order.customerPhone
            )
        
        db.session.add(service)

        Order.query.filter_by(id=order.id).delete()

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'error'
        
        return redirect(url_for('service.servicePage'),code=302)

    else:
        return render_template('Service/confirmOrder.html',form=form)


@service.route('/del-order/<id>')
@login_required
def delOrder(id):
    Order.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("service.servicePage"))

@service.route('/del-service/<id>')
@login_required
def delService(id):
    Service.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("service.servicePage"))


