import telebot
from decouple import config
from pymysql.cursors import DictCursor  # Возвразает курсор в виде словаря из базы данных
import pymysql.connections
import pymysql  # модуль работы с MySQL

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
fault_list = []
for j in cur.fetchall():
    print(f'Server: {j["name"]}, fault: {j["fault_name"]}')
    fault_list.append(j)
# for i in fault_list:
#     print(f'')
# print(fault_list)
