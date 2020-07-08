from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import NeedsForm, GiverForm
from app.models import Komek
from app import db
from sqlalchemy import text
import inspect

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')

@app.route('/confirmed')
def confirmed():
    id = request.args.get('id')
    phone = request.args.get('phone')

    if id is None or id == '' or phone is None or phone == '':
        return render_template('index.html', title='Главная страница')

    return render_template('confirmed.html', title='Оформлено', id=id, phone=phone)

@app.route('/needs', methods=['GET', 'POST'])
def needs():
    form = NeedsForm()
    if form.validate_on_submit():
        komek = Komek(name=form.name.data, phone=form.phone.data, 
        city=form.city.data, service=form.needs.data, is_giver=False, flag=1)
        db.session.add(komek)
        db.session.commit()
        return redirect(url_for('confirmed', id=komek.id, phone=komek.phone))
    return render_template('needs.html', title='Нужна помощь', form=form)

@app.route('/giver', methods=['GET', 'POST'])
def giver():
    form = GiverForm()
    if form.validate_on_submit():
        komek = Komek(name=form.name.data, phone=form.phone.data, 
        city=form.city.data, service=form.gift.data, is_giver=True, flag=1)
        db.session.add(komek)
        db.session.commit()
        return redirect(url_for('confirmed', id=komek.id, phone=komek.phone))
    return render_template('giver.html', title='Могу помочь', form=form)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        phone = request.form['phone']

        if id == 0 or phone is None or phone == '':
            errors = ["Не все поля заполнены"]
            return render_template('update.html', title='Обновить профиль', errors=errors)
        
        sql = f"UPDATE Komek SET flag = 0 WHERE id = {id} AND komek.phone = '{phone}'"
        result = db.engine.execute(text(sql))

        return render_template('index.html', title='Главная страница', updated=True)

    return render_template('update.html', title='Обновить профиль', errors=None)

@app.route('/global')
def global_app():
    page = request.args.get('page', 1, type=int)
    service = request.args.get('service')
    city = request.args.get('city')
    is_giver = request.args.get('is_giver')

    form = {'service':'', 'city':'', 'is_giver':''}

    sql = 'SELECT komek.id AS komek_id, komek.name AS komek_name, komek.phone AS komek_phone, komek.city AS komek_city, komek.service AS komek_service, komek.is_giver AS komek_is_giver, komek.flag AS komek_flag FROM komek'

    if is_giver is not None and is_giver != '':
        sql += f" WHERE komek.is_giver IS {int(is_giver == 'True')}"
        form['is_giver'] = (is_giver == 'True')

    if city is not None and city != '':
        sql += f" AND komek.city LIKE '%{city.lower()}%'"
        form['city'] = city

    if service is not None and service != '':
        sql += f" AND komek.service LIKE '%{service}%'"
        form['service'] = service

    has_next = db.engine.execute(text(sql + f" limit {app.config['POSTS_PER_PAGE']} offset {app.config['POSTS_PER_PAGE'] * page}"))

    next_url = url_for('global_app', page=page+1, service=service, city=city, is_giver=is_giver) if len([row for row in has_next]) > 0 else None
    prev_url = url_for('global_app', page=page-1, service=service, city=city, is_giver=is_giver) if page > 1 else None

    result = [jsonify(row) for row in db.engine.execute(text(sql + f" limit {app.config['POSTS_PER_PAGE']} offset {app.config['POSTS_PER_PAGE'] * (page - 1)}"))]
    
    return render_template('global.html', title='Глобальный поиск', helps=result, form=form, next_url=next_url, prev_url=prev_url)

def jsonify(row):
    return {
        "id" : row[0],
        "name" : row[1],
        "phone" : row[2],
        "city": row[3],
        "service": row[4],
        "is_giver": row[5],
        "flag": row[6]
    }