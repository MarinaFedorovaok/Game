from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
import commands as c
import my_bot_api

updater = Updater(my_bot_api.api) # Создайте файл my_bot_api.py(добавлен в игнор) и в переменную api положите ваш код
print("Server started")

updater.dispatcher.add_handler(CommandHandler('buttom', c.start_buttom))
updater.dispatcher.add_handler(CallbackQueryHandler(c.button))

updater.dispatcher.add_handler(CommandHandler('start', c.help))
updater.dispatcher.add_handler(CommandHandler('help', c.help))
updater.dispatcher.add_handler(CommandHandler('stats', c.stats))
updater.dispatcher.add_handler(CommandHandler('run', c.run))
updater.dispatcher.add_handler(MessageHandler(Filters.text, c.turn))
updater.dispatcher.add_handler(MessageHandler(Filters.command, c.unknown))

updater.start_polling()
updater.idle()