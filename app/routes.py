from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import NeedsForm, GiverForm
from app.models import Komek
from app import db
# from functions import get_vacancies, get_vacancy_by_id

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
        return redirect(url_for('global_app', service=komek.service, city=komek.city))
    return render_template('needs.html', title='Нужна помощь', form=form)

@app.route('/giver', methods=['GET', 'POST'])
def giver():
    form = GiverForm()
    if form.validate_on_submit():
        komek = Komek(name=form.name.data, phone=form.phone.data, 
        city=form.city.data, service=form.gift.data, is_giver=True, flag=1)
        db.session.add(komek)
        db.session.commit()
        return redirect(url_for('global_app', service=komek.service, city=komek.city))
    return render_template('giver.html', title='Могу помочь', form=form)

@app.route('/global')
def global_app():
    service = str(request.args.get('service'))
    city = str(request.args.get('city'))
    is_giver = request.args.get('is_giver') == 'True'

    helps = Komek.query.filter(Komek.city==city, Komek.is_giver==(not is_giver))
    helps = [help for help in helps if service in help.service]
    return render_template('global.html', title='Глобальный поиск', helps=helps)
    