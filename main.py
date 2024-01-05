# <---------- Импорт сторонних функций  ---------->
import asyncio


# <---------- Импорт локальных функций ---------->
from create_bot import dp, bot, psql, mndb
from handlers.routers import *

from handlers.private import client, schedule
from handlers.group import group

from utilities.ut_logger import ut_LogStart
from handlers.private import client


# <---------- Переменные ---------->
filename = 'main.py'


# <---------- Функции on_startup и on_shutdown ---------->
async def on_startup():
	"""
	Initializing all connections.
	"""
	print('\n- - - HomeWorker is online - - -')
	if ut_LogStart():
		print('Logger started OK!')
	if psql:
		print('PostgreSQL connection OK!')
	if mndb:
		print('MongoDB connection OK!')
	print()


async def on_shutdown():
	"""
	Closing all connections.
	"""
	print()
	await psql.close()
	await mndb.close()
	print('Goodbye...')


# <---------- Запуск бота ---------->
async def main():
	"""
	- StartUp/ShutDown.
	- Router registration.
	- Delete WebHook.
	- Start polling.
	"""
	dp.startup.register(on_startup)
	dp.shutdown.register(on_shutdown)

	dp.include_routers(router_registered, router_unregistered)

	client.register_handlers(router_private)
	schedule.register_handlers(router_private_admin)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
