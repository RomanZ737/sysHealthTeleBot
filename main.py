import telebot
from telebot import types
from decouple import config
from pymysql.cursors import DictCursor  # Возвразает курсор в виде словаря из базы данных
import pymysql.connections
import pymysql  # модуль работы с MySQL

token = config("sys_health_bot_taken", default='')
chat_id = config("sys_health_bot_chat_id", default='')
bot = telebot.TeleBot(token)

keyButton = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton(text='FAULTS', callback_data='/faults')
#btn2 = types.InlineKeyboardButton(text='Temp')

keyButton.add(btn1)


# def start():
#     bot.send_message(chat_id=chat_id, text='Hello', reply_markup=markup)
#
# start()

@bot.message_handler(content_types=['text'])
def text_test(message):
    #bot.send_message(message.chat.id, "Test button", reply_markup=keyButton)
    if message.text == 'FAULTS':
        bot.send_message(message.chat.id, "Here is some info")

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Hello', reply_markup=keyButton)


@bot.message_handler(commands=['faults'])  # формирует список активных ошибок и базы данных
def fault_list(message):
    """MySQL Connection Block"""
    connection = pymysql.connect(  # Коннектимся к базе MySQL
        host=config('ip_mysql', default=''),
        user=config("SQL_usrID", default=''),
        password=config('SQL_password', default=''),
        db=config('SQL_DB', default=''),
        charset='utf8mb4',
        cursorclass=DictCursor  # Курсор будет возвращать значения в виде словарей
    )
    cur = connection.cursor()  # Создаём курсор SQL
    request = f"SELECT * FROM other_faults"
    cur.execute(request)
    for j in cur.fetchall():
        bot.send_message(message.from_user.id, (f'Server: {j["name"]}, fault: {j["fault_name"]}'))
    connection.commit()


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     bot.send_message(message.from_user.id, message)
# if message.text == "Привет":
#     bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
# elif message.text == "/help":
#     bot.send_message(message.from_user.id, "Напиши привет")
# else:
#     bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
