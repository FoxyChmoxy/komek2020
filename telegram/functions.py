from telegram import Bot
from telegram.ext import Updater
from telegram import ReplyKeyboardMarkup
from telegram import ParseMode
from sqlalchemy import create_engine
import sqlalchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
help_button = 'Помощь | Көмек'
info_button = 'Информация | Ақпарат'

def send_message_with_reply(bot: Bot, update: Updater, text: str, 
reply_markup: ReplyKeyboardMarkup):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = text,
        reply_markup = reply_markup)

def send_message(bot: Bot, update: Updater, text: str):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = text, parse_mode='HTML')

def get_values(is_giver):
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))
    with engine.connect() as con:
        sql = sqlalchemy.text(f"select * from komek WHERE komek.is_giver IS {int(is_giver)} LIMIT 10")
        result = con.execute(sql)
        table = [jsonify(row) for row in result]
        text = ''

        for row in table:
            text += f'Имя: {row["name"]} \n'
            text += f'Телефон: {row["phone"]} \n'
            text += f'Город: {row["city"]} \n'
            text += f'Что нужно | Может дать: {row["service"]} \n\n'
        
        return text

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