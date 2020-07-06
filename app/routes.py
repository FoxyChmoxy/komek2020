from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import NeedsForm, GiverForm
from app.models import Komek
from app import db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')

@app.route('/needs', methods=['GET', 'POST'])
def needs():
    form = NeedsForm()
    if form.validate_on_submit():
        komek = Komek(name=form.name.data, phone=form.phone.data, 
        city=form.city.data, service=form.needs.data, is_giver=False, flag=1)
        db.session.add(komek)
        db.session.commit()
        return redirect(url_for('global_app', service=komek.service, city=komek.city, is_giver=True))
    return render_template('needs.html', title='Нужна помощь', form=form)

@app.route('/giver', methods=['GET', 'POST'])
def giver():
    form = GiverForm()
    if form.validate_on_submit():
        komek = Komek(name=form.name.data, phone=form.phone.data, 
        city=form.city.data, service=form.gift.data, is_giver=True, flag=1)
        db.session.add(komek)
        db.session.commit()
        return redirect(url_for('global_app', service=komek.service, city=komek.city, is_giver=False))
    return render_template('giver.html', title='Могу помочь', form=form)

@app.route('/global')
def global_app():
    service = request.args.get('service')
    city = request.args.get('city')
    is_giver = request.args.get('is_giver')

    result = Komek.query.all()

    if city is not None:
        result = [obj for obj in result if obj.city == city.lower()]

    if is_giver is not None:
        result = [obj for obj in result if obj.is_giver == (is_giver == 'True')]

    if service is not None:
        result = [obj for obj in result if service in obj.service]
    
    return render_template('global.html', title='Глобальный поиск', helps=result)
    