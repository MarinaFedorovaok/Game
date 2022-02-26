from email import message
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from random import randint


database = {} # БД вида {ID:[Имя, банк, побед, поражений]}
bank = 1 # номер элемента списка в БД


# проверка ввода корректной команды
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(f'Я вот прям не знаю как на это ваше "{update.message.text}" \
реагировать... Расслабьтесь, почитайте /help')


# вывод статистики игрока
def stats(update: Update, context: CallbackContext):
    user(update, context)
    update.message.reply_text(f'{update.effective_user.first_name}, количество ваших побед: \
{database[update.effective_user.id][2]}\nколичество поражений: {database[update.effective_user.id][3]}\
\n\nХотите сыграть ещё? На столе спичек: {database[update.effective_user.id][bank]}, сколько берёте?')


def help(update: Update, context: CallbackContext):
    user(update, context)
    update.message.reply_text(f'Приветствую {update.effective_user.first_name}, это простая игра. \
На столе лежат спички, их {database[update.effective_user.id][bank]}. Вы можете брать от \
1 до 4 спичек за ход.\nПобедит тот, кто заберёт последнюю.\nСколько штук возьмёте?')


# проверка и добавление пользователя в БД
def user(update: Update, context: CallbackContext):
    if update.effective_user.id not in database:
        database.update({update.effective_user.id:[update.effective_user.first_name, 21, 0, 0]})


# ход игрока
def turn(update: Update, context: CallbackContext):
    user(update, context)
    msg = update.message.text
    if input_check(msg): #  проверка ввода
        database[update.effective_user.id][bank] -= int(msg)
        if database[update.effective_user.id][bank] <= 0: # проверка на победу
            update.message.reply_text('Вы берёте последнюю спичку и побеждаете в игре!\n\
Команда /stats покажет вашу статистику игр.')
            database[update.effective_user.id][2] += 1 # счётчик побед
            database[update.effective_user.id][bank] = 21
            update.message.reply_text('Я снова насыпал 21 спичку на стол и прошу реванш!\n\
Сколько спичек возьмёте?')
            return
        update.message.reply_text(f'Осталось спичек: {database[update.effective_user.id][bank]}, \
ходит бот.')
        bot_turn(update, context)
    else:
        unknown(update, context)
        

# ход бота
def bot_turn(update: Update, context: CallbackContext):
    bot_take = bot_logic(database[update.effective_user.id][bank])
    if bot_take == 1:
        s = 'спичку'
    else:
        s = 'спички'
    update.message.reply_text(f'Бот забирает {bot_take} {s}')
    database[update.effective_user.id][bank] -= bot_take
    if database[update.effective_user.id][bank] <= 0: # проверка на проигрыш
        update.message.reply_text(f'Вы проиграли, бот забрал последнюю спичку...\n\
Команда /stats покажет вашу статистику игр.')
        database[update.effective_user.id][3] += 1 # счётчик поражений
        database[update.effective_user.id][bank] = 21
        update.message.reply_text('Я ещё не устал и могу сыграть снова. На столе опять 21 спичка.\n\
Сколько возьмёте?')
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
        return 1 <= int(msg) <= 4
    except:
        return 0
