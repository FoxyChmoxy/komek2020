from telegram import Bot
from telegram.ext import Updater
from telegram import ReplyKeyboardMarkup

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
        text = text)