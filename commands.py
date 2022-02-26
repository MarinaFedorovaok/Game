from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from random import randint


database = {} # БД вида {ID:[Имя, банк, побед, поражений]}
bank = 1 # номер элемента списка в БД


# проверка ввода корректной команды
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(f'Я вот прям не знаю как на это ваше {update.message.text} реагировать... Расслабьтесь, почитайте /help')


# вывод статистики игрока
def stats(update, context):
    update.message.reply_text(f'{update.effective_user.first_name}, количество ваших побед: {database[update.effective_user.id][2]}\nколичество поражений: {database[update.effective_user.id][3]}\n\nХотите сыграть ещё? Нажмите /run')


def help(update: Update, context: CallbackContext):
    update.message.reply_text(f'{update.effective_user.first_name}, это простая игра. На столе лежит 21 спичка, вы можете брать от 1 до 4 спичек за ход.\n\
Победит тот, кто заберёт последнюю.\nДля начала игры пришлите команду /run')


# проверка и добавление пользователя в БД
def user(update, context):
    if update.effective_user.id not in database:
        database.update({update.effective_user.id : [update.effective_user.first_name, 21, 0, 0]})
 

# запуск игры 
def run(update: Update, context: CallbackContext):
    user(update, context)
    if database[update.effective_user.id][bank] <= 0: # если банк игрока пуст
            database[update.effective_user.id][bank] = 21 # то обновить его
    update.message.reply_text(f'Приветствую {update.effective_user.first_name}!\nВсего спичек на столе: {database[update.effective_user.id][bank]}\nОтправьте количество спичек, которые хотите забрать.')


# ход игрока
def turn(update: Update, context: CallbackContext):
    user(update, context)
    database[update.effective_user.id][bank] -= int(update.message.text)
    if database[update.effective_user.id][bank] <= 0:
        update.message.reply_text(f'Вы берёте последнюю спичку и побеждаете в игре!\nКоманда /run начнёт новую игру.\nКоманда /stats покажет вашу статистику игр.')
        database[update.effective_user.id][2] += 1 # счётчик побед
        return
    update.message.reply_text(f'Осталось спичек: {database[update.effective_user.id][bank]}, ходит бот.')
    bot_turn(update, context)

# ход бота
def bot_turn(update: Update, context: CallbackContext):
    bot_take = bot_logic(database[update.effective_user.id][bank])
    if bot_take == 1:
        s = 'спичку'
    else:
        s = 'спички'
    update.message.reply_text(f'Бот забирает {bot_take} {s}')
    database[update.effective_user.id][bank] -= bot_take
    if database[update.effective_user.id][bank] <= 0:
        update.message.reply_text(f'Вы проиграли, бот забрал последнюю спичку...\nКоманда /run начнёт новую игру!\nКоманда /stats покажет вашу статистику игр.')
        database[update.effective_user.id][3] += 1 # счётчик поражений
        return
    update.message.reply_text(f'Осталось спичек: {database[update.effective_user.id][bank]}')


def bot_logic(s):
    if not s % 5:
        return randint(1, 4)
    else:
        return s % 5


#  проверка ввода
def input_check(msg):
    try:
        return 1 <= int(msg.split()[1]) <= 4
    except:
        return 0
