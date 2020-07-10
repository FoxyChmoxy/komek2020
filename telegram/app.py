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
from functions import send_message, send_message_with_reply, get_values

CONFIG = Config("tg.config.json").data
TG_CONFIG = CONFIG['telegram']
OFFSET = {
    "giver" : 0,
    "needs" : 0
}

def button_help_handler(bot:Bot, update: Updater, is_giver: bool, offset: int):
    send_message(bot, update, get_values(is_giver, offset))

def message_handler(bot: Bot, update: Updater):
    '''
        Вернуть пользователю результат его поиска по заданному тексту.
    '''
    
    text = update.message.text
    result = CONFIG['bot']["default_text"]

    try:
        if text == CONFIG['bot']['help_btn']:
            OFFSET["needs"] += 1
            return button_help_handler(bot, update, False, OFFSET["needs"])
        if text == CONFIG['bot']['giver_btn']:
            OFFSET["giver"] += 1
            return button_help_handler(bot, update, True, OFFSET["giver"])
    except:
        pass
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=CONFIG['bot']['help_btn']),
                KeyboardButton(text=CONFIG['bot']['giver_btn'])
            ]
        ],
        resize_keyboard=True
    )

    send_message_with_reply(bot, update, CONFIG['bot']["default_text"], reply_markup)



# def set_start_handler(updater):
#     '''
#         Задать стартового обработчика.
#     '''
#     handler = CommandHandler("start", start_handler)
#     updater.dispatcher.add_handler(handler)

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
    # set_start_handler(updater)
    set_message_handler(updater)

def main():
    bot = Bot(token=TG_CONFIG['token'])
    updater = Updater(bot=bot)

    set_all_handlers(updater)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()