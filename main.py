# <---------- Импорт функций Aiogram ---------->
from aiogram.utils import executor


# <---------- Импорт локальных функций ---------->
from create_bot import dp
from handlers import client, group
from data_base.operation import db_PsqlStart, db_MongoDbStart
from utilities.ut_logger import ut_LogStart, ut_LogCreate


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
	if db_PsqlStart():
		await ut_LogCreate(
			id=00000000,
			filename=filename,
			function='on_startup',
			exception='',
			content='Database PSQL connected!'
		)
	if db_MongoDbStart():
		await ut_LogCreate(
			id=00000000,
			filename=filename,
			function='on_startup',
			exception='',
			content='Database MongoDB connected!'
		)


async def on_shutdown(_):
	pass


# <---------- Основные функции ---------->
client.register_handlers_client(dp)
group.register_handlers_group(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
