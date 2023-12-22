# <---------- Импорт функций Aiogram ---------->
from aiogram.utils import executor


# <---------- Импорт локальных функций ---------->
from create_bot import dp, db_host, db_user, db_password, db_name
from handlers import client, group
from data_base.operation import db_PsqlStart, db_MongoDbStart
from utilities.ut_logger import ut_LogStart


# <---------- Переменные ---------->
filename = 'main.py'


# <---------- Функции on_startup и on_shutdown ---------->
async def on_startup(_):
	"""
	Инициализация всех подключений
	:param _:
	:return:
	"""
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
client.register_handlers_client(dp)
group.register_handlers_group(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
