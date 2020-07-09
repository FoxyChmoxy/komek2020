from config import Config
import requests
from telegram import Bot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import KeyboardButton
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from functions import send_message, send_message_with_reply, help_button, info_button

CONFIG = Config("tg.config.json").data
TG_CONFIG = CONFIG['telegram']

def start_handler(bot: Bot, update: Updater):
    '''
        Отправить пользователю приветственные слова.
        Работает через команду '/start'.
    '''
    send_message(bot, update, CONFIG['bot']['start_text'])

def button_help_handler(bot:Bot, update: Updater):
    send_message(bot, update, CONFIG['bot']['help_text'])

def message_handler(bot: Bot, update: Updater):
    '''
        Вернуть пользователю результат его поиска по заданному тексту.
    '''
    
    text = update.message.text
    result = CONFIG['bot']["default_text"]

    try:
        if text == help_button:
            return button_help_handler(bot, update)
        if text == info_button:
            return start_handler(bot, update)
    except:
        pass
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=info_button),
                KeyboardButton(text=help_button)
            ]
        ],
        resize_keyboard=True
    )

    send_message_with_reply(bot, update, CONFIG['bot']["default_text"], reply_markup)



def set_start_handler(updater):
    '''
        Задать стартового обработчика.
    '''
    handler = CommandHandler("start", start_handler)
    updater.dispatcher.add_handler(handler)

def set_message_handler(updater):
    '''
        Задать обработчика сообщений.
    '''
    handler = MessageHandler(Filters.text, message_handler)
    updater.dispatcher.add_handler(handler)

def set_all_handlers(updater):
    '''
        Задать все необходимые обработчики для телеграм-бота.
    '''
    set_start_handler(updater)
    set_message_handler(updater)

def main():
    bot = Bot(token=TG_CONFIG['token'])
    updater = Updater(bot=bot)

    set_all_handlers(updater)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()