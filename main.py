import time
from telegram import Bot, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext.updater import Updater
import requests


# Joke Model
class Joke:
    def __init__(self, id_, type, setup, punchline):
        self.id_ = id_
        self.type = type
        self.setup = setup
        self.punchline = punchline

    @staticmethod
    def factory(data):
        return Joke(
            id_=data["id"],
            type=data["type"],
            setup=data["setup"],
            punchline=data["punchline"]
        )


# Joke Model
def getRandomJoke():
    response = requests.get("https://official-joke-api.appspot.com/jokes/random")
    joke_data = response.json()
    return joke_data


updater = Updater("1441599085:AAGTevbvJPA9vSbflWCJZQey4eFMstsf4Dc", use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    kbd_lst = [["Random Joke"], ["Developer"]]
    kbd = ReplyKeyboardMarkup(kbd_lst)

    update.message.reply_text(text="Are you ready to laugh?\nChoose Options", reply_markup=kbd)


def getJoke(update, context):
    joke = getRandomJoke()
    joke = Joke.factory(data=joke)
    keyboard = [[
        InlineKeyboardButton("Punch", callback_data=str(joke.punchline)), ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=joke.setup, reply_markup=reply_markup)


def punch(update, context):
    query = update.callback_query
    query.answer()
    punch_line = query.data
    query.edit_message_text(text=punch_line)


def developer(update, context):
    update.message.reply_text(text="Absera Temesgen")


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text("Random Joke"), getJoke))
updater.dispatcher.add_handler(CallbackQueryHandler(punch))
dispatcher.add_handler(MessageHandler(Filters.text("Developer"), developer))

updater.start_polling()
print("...")
