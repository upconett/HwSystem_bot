# <---------- Импорт функций Aiogram ---------->
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# <---------- Импорт локальных функций ---------->
from config import TOKEN


# <---------- Основные функции ---------->
storage = MemoryStorage()


bot = Bot(token=TOKEN, parse_mode='Markdown')
dp = Dispatcher(bot, storage=storage)
