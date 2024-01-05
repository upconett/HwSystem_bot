# <---------- Python modules ---------->
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


# <---------- Local modules ---------->
from utilities import ut_configuration
from data_base.db_psql import PostgreSQL
from data_base.db_mongo import MongoDB


# <---------- Main ---------->
storage = MemoryStorage()
exception_data = (0, 0, 0, 0, 0, 0, 0, 0, 0)

config = ut_configuration.startupConfiguration()
if config != exception_data:
    MAIN_TOKEN, LOG_TOKEN, creators, api_hash, api_id, db_host, db_user, db_password, db_name = config
else:
    quit()

psql = PostgreSQL(host=db_host, user=db_user, password=db_password, database=db_name)
mndb = MongoDB(host=db_host, user=db_user, password=db_password, database=db_name)

bot = Bot(token=MAIN_TOKEN, parse_mode='html', disable_web_page_preview=True)
dp = Dispatcher(storage=storage)
