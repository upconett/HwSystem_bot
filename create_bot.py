# <---------- Импорт функций Aiogram ---------->
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# <---------- Импорт локальных функций ---------->
from utilities.ut_configuration import ut_startupConfiguration
from data_base.db_psql import PostgreSQL
from data_base.db_mongo import MongoDB


# <---------- Основные функции ---------->
storage = MemoryStorage()
exception_data = (0, 0, 0, 0, 0, 0, 0, 0, 0)

config = ut_startupConfiguration()
if config != exception_data:
    MAIN_TOKEN, LOG_TOKEN, creators, api_hash, api_id, db_host, db_user, db_password, db_name = config
else:
    quit()

psql = PostgreSQL(host=db_host, user=db_user, password=db_password, database=db_name)
mndb = MongoDB(host=db_host, user=db_user, password=db_password, database=db_name)

bot = Bot(token=MAIN_TOKEN, parse_mode='html', disable_web_page_preview=True)
dp = Dispatcher(bot, storage=storage)
