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

server_data = []  # реальные имена и данные серверов и устройств


def start():
    bot.send_message(chat_id=chat_id, text='Bot Started', reply_markup=keyButton)
    """MySQL Connection Block"""  # Выгружаем в словарь реальные имена и данные серверов и устройств
    connection = pymysql.connect(  # Коннектимся к базе MySQL
        host=config('ip_mysql', default=''),
        user=config("SQL_usrID", default=''),
        password=config('SQL_password', default=''),
        db=config('SQL_DB', default=''),
        charset='utf8mb4',
        #        cursorclass=DictCursor  # Курсор будет возвращать значения в виде словарей
    )
    cur = connection.cursor()  # Создаём курсор SQL
    sql_request = "SELECT * FROM real_name"
    cur.execute(sql_request)
    for i in (cur.fetchall()):  # Создаём список картежей с данными серверов и сетевых устройств
        server_data.append(i)
    connection.close()

start()  # Функция выполняет действия необходимые только при запуске/перезапуске бота


# @bot.message_handler(commands=['text'])

@bot.message_handler(content_types=['text'])
def text_test(message):
    if message.text == 'Faults':    # Выгружаем активные ошибки, если они имеются
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
        if len(cur.fetchall()) > 0:
            for j in cur.fetchall():
                for l in server_data:
                    if j["name"] in l:
                        text = f'❌ FAULT:\nServer: <b>{l[2]}</b> (IP {l[3]})\nFAULT: <b>{j["fault_name"]}</b>'
                        bot.send_message(message.from_user.id, text, parse_mode='html')
            connection.close()
        else:
            text = '✅ <b>NO FAULTS DETECTED</b>'
            bot.send_message(message.from_user.id, text, parse_mode='html')
    else:
        text = 'Нет такой команды'
        bot.send_message(message.from_user.id, text, parse_mode='html')

# ✅ FIXED\n


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
