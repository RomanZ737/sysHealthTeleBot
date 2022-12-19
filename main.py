import telebot
from telebot import types
from decouple import config
from pymysql.cursors import DictCursor  # Возвразает курсор в виде словаря из базы данных
import pymysql.connections
import pymysql  # модуль работы с MySQL

token = config("sys_health_bot_taken", default='')
chat_id = config("sys_health_bot_chat_id", default='')
bot = telebot.TeleBot(token)

keyButton = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
faults_button = types.KeyboardButton(text='Faults')
status_button = types.KeyboardButton(text='Server Status')

keyButton.add(faults_button, status_button)


def start():
     bot.send_message(chat_id=chat_id, text='Hello', reply_markup=keyButton)

start()

@bot.message_handler(content_types=['text'])
def text_test(message):
    #bot.send_message(message.chat.id, "Test button", reply_markup=keyButton)
    if message.text == 'Faults':
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
            text = f'❌ FAULT:\nServer: <b>{j["name"]}</b>, fault: <b>{j["fault_name"]}</b>'
            bot.send_message(message.from_user.id, text, parse_mode='html')
            #bot.send_message(message.from_user.id, (f'Server: {j["name"]}, fault: {j["fault_name"]}'))
        connection.commit()
#✅ FIXED\n


# @bot.message_handler(commands=['faults'])  # формирует список активных ошибок и базы данных
# def fault_list(message):



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
