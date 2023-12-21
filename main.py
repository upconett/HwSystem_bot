# <---------- Импорт функций Aiogram ---------->
from aiogram.utils import executor


# <---------- Импорт локальных функций ---------->
import create_bot
from handlers import client, group
from data_base.operation import db_PsqlStart, db_MongoDbStart
from utilities.ut_logger import ut_LogStart


# <---------- Переменные ---------->
filename = 'main.py'
db_host = create_bot.db_host
db_user = create_bot.db_user
db_password = create_bot.db_password
db_name = create_bot.db_name


# <---------- Функции on_startup и on_shutdown ---------->
async def on_startup(_):
	"""
	Инициализация всех подключений
	:param _:
	:return:
	"""
	print()
	print(' - - - HomeWorker is online - - -')
	if ut_LogStart():
		print('Logger started OK!')
	if db_PsqlStart(db_host, db_user, db_password, db_name):
		print('PSQL started OK!')
	if db_MongoDbStart(db_host, db_user, db_password, db_name):
		print('MongoDB started OK!')


async def on_shutdown(_):
	pass


# <---------- Основные функции ---------->
client.register_handlers_client(create_bot.dp)
group.register_handlers_group(create_bot.dp)


executor.start_polling(create_bot.dp, skip_updates=True, on_startup=on_startup)
