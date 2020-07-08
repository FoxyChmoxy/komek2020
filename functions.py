#!/usr/bin/python

import sys
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from app.models import Komek
from app import db
import os
import numpy as np


URL = "https://docs.google.com/spreadsheets/u/0/d/18Zt-cliIAa6C8TPgYBFJ5kowPviNjrsYFx73hcBHmHQ/htmlview?pru=AAABc0bssiI*ebaWGE4n-KBXIEpxPXobGQ"
DATETIME_FORMAT = "%Y-%m-%d-%H.%M.%S"

def get_table():
    '''
    Запрос на заполучение всех данных из существующей Google таблицы
    '''
    print("Запрос на docs.google.com...")
    response = requests.get(URL)
    if response.ok:
        print("Запрос успешно обработан!")
        today = datetime.today().strftime(DATETIME_FORMAT)
        with open(f"docs/{today}_docs.txt", "w") as file:
            print("Создается новый table-doc файл...")
            file.write(response.text)
            print("Новый table-doc файл успешно создан!")

def drop_database():
    files = os.listdir()
    for file in files:
        print("Поиск локальной базы данных...")
        if(file == 'app.db'):
            os.remove(file)
            print("Старая версия базы данных удалена.")
            break

def create_database():
    os.system('flask db upgrade')
    print("Создалась новая версия базы данных!")

def fill_database():
    '''
    Заполнить БД данными из последннего выкаченного файла
    '''
    last_doc = get_last_doc_file()
    with open(f"docs/{last_doc}", "r") as doc:
        print("Поиск нужных записей из table-doc файла...")
        html = doc.read()
        soup = BeautifulSoup(html, 'html.parser')
        table = np.array(soup.findAll('tr'))
    
    print("Обработка и запись данных...")
    for row in table[4:]:
        data = row.findAll('td')
        if has_required_data(data, flag=True):
            komek = create_needs(data[0].text, data[1].text, data[2].text, data[3].text)
            db.session.add(komek)
            db.session.commit()
            print(komek.__repr__())
        if has_required_data(data, flag=False):
            komek = create_giver(data[6].text, data[7].text, data[8].text, data[9].text)
            db.session.add(komek)
            db.session.commit()
            print(komek.__repr__())
    print("Все данные успешно записаны!")

def has_required_data(data, flag):
    '''
    Имеет ли запись необходимые данные
    :param data: (bs4.obj.tag)
    :param flag: (bool)
    '''
    if flag:
        conditions = [has_data(data[0]), has_data(data[1]), has_data(data[2]), has_data(data[3])]
    else:
        conditions = [has_data(data[6]), has_data(data[7]), has_data(data[8]), has_data(data[9])]
    return len([0 for cond in conditions if cond == True]) > 0

def has_data(data):
    try:
        result = data.text.strip() != '' and len(data.text.strip()) > 1
        return result
    except:
        return False

def create_needs(name, phone, city, needs):
    return create_komek(name, phone, city, needs, False, True)

def create_giver(name, phone, city, needs):
    return create_komek(name, phone, city, needs, True, True)

def create_komek(name, phone, city, needs, is_giver, flag):
    return Komek(name=name, phone=phone, city=city.lower(), service=needs, is_giver=is_giver, flag=flag)

def get_last_doc_file():
    '''
    Получить последний скачанный файл
    '''
    dates = []
    for file in os.listdir('docs'):
        dates.append(get_datetime(file))
    return max(dates).strftime(DATETIME_FORMAT) + "_docs.txt"

def get_datetime(file_name):
    '''
    Возвращает дату из названия файла
    '''
    return datetime.strptime(file_name.split('_')[0], DATETIME_FORMAT)

def get_all_givers():
    print_all(Komek.query.filter_by(is_giver=True))

def get_all_needs():
    print_all(Komek.query.filter_by(is_giver=False))
        

def print_all(result):
    for komek in result:
        print(komek.id)
        print(komek.name)
        print(komek.phone)
        print(komek.city)
        print(komek.service)
        print(f"flag: {komek.flag}")
        print('--------------')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            get_table()
            create_database()
            fill_database()
        elif sys.argv[1] == 'db':
            drop_database()
            create_database()
            fill_database()
        elif sys.argv[1] == 'refresh':
            get_table()
            drop_database()
            create_database()
            fill_database()
        elif sys.argv[1] == 'givers':
            get_all_givers()
        elif sys.argv[1] == 'needs':
            get_all_needs()
