# <---------- Импорт функций Aiogram ---------->
from aiogram.utils import executor

# <---------- Импорт локальных функций ---------->
from create_bot import dp
from handlers import client, group


async def on_startup(_):
	print(' - - - HomeWorker is here - - -')


client.register_handlers_commands(dp)
group.register_handlers_student(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)