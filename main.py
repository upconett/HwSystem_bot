# <---------- Импорт сторонних функций  ---------->
import asyncio


# <---------- Импорт локальных функций ---------->
from create_bot import dp, bot, psql, mndb
from handlers import client, group, schedule
from utilities.ut_logger import ut_LogStart


# <---------- Переменные ---------->
filename = 'main.py'


# <---------- Функции on_startup, main и on_shutdown ---------->
async def on_startup():
	"""
	Initializing all connections.
	:param _:
	:return:
	"""
	print('\n- - - HomeWorker is online - - -')
	if ut_LogStart():
		print('Logger started OK!')
	if psql:
		print('PostgreSQL started OK!')
	if mndb:
		print('MongoDB started OK!')
	print()


async def main():
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


async def on_shutdown():
	print()
	await psql.close()
	await mndb.close()
	print('Goodbye...')


# <---------- Основные функции ---------->
schedule.register_handlers_schedule(dp)
client.register_handlers_client(dp)
group.register_handlers_group(dp)


# <---------- Запуск бота ---------->
if __name__ == '__main__':
	try:
		asyncio.run(on_startup())
		asyncio.run(main())
	except:
		asyncio.run(on_shutdown())