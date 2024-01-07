# <---------- Python modules  ---------->
import asyncio


# <---------- Local modules ---------->
from create_bot import dp, bot, psql, mndb
from handlers.routers import *
from handlers.private import commands, default_schedule_upload, group_create
from handlers.group import group, homework_upload
from utilities import ut_logger


# <---------- on_startup & on_shutdown functions ---------->
async def on_startup():
	"""
	Initializing all connections.
	"""
	print('\n- - - HomeWorker is online - - -')
	if ut_logger.start_logger():
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


# <---------- Bot start ---------->
async def main():
	"""
	- StartUp/ShutDown.
	- Router registration.
	- Delete WebHook.
	- Start polling.
	"""
	dp.startup.register(on_startup)
	dp.shutdown.register(on_shutdown)

	dp.include_routers(
		router_chat_complex,
		router_private_groupAdmin,
		router_chat,
		router_private,
		router_unregistered,
		router_base
	)

	commands.register_handlers(router=router_private)
	group.register_handlers(
		router0=router_chat,
		router1=router_chat_complex
	)
	homework_upload.register_handlers(router=router_chat_in_group)
	group_create.register_handlers(router=router_private)
	default_schedule_upload.register_handlers(router=router_private_groupAdmin)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
