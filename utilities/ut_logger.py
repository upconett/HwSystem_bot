# <---------- Импорт сторонних функций ---------->
import logging

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


# <---------- Импорт локальных функций ---------->
from data_base.operation import db_psql_UserData


# <---------- Переменные ---------->
logger = None


# <---------- Основные функции ---------->
def ut_LogStart():
	"""
	Creating logger object.
	:return: True or False based on the result of creating the logger
	"""
	try:
		global logger
		logger = logging.getLogger(__name__)
		logger.setLevel(logging.INFO)
		Path(r"logs").mkdir(parents=True, exist_ok=True)
		log_filename = f'logs/{datetime.now().strftime("%Y-%m-%d")}_log.log'
		handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, encoding='utf-8')
		handler.suffix = "%Y-%m-%d"
		handler.setLevel(logging.INFO)

		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
		handler.setFormatter(formatter)

		logger.addHandler(handler)
		return True
	except Exception as exception:
		print(f'Logger not created. Exception "{exception}".')
		return False


async def ut_LogCreate(id: int, filename: str, function: str, exception, content: str):
	"""
	Creating new log.
	:param id: User ID from telegram
	:param filename: File name
	:param function: Function name
	:param exception: Exception or str object
	:param content:
	:return:
	"""
	if id == 00000000:
		data = {
			'username': 'bot',
		}
	else:
		data = await db_psql_UserData(id=id)
	date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	log_message = f'DATA={data}; FILENAME="{filename}"; FUNCTION="{function}"; CONTENT="{content}"; EXCEPTION="{exception}";'
	print(f'DATE="{date}"; {log_message}')
	logger.info(log_message)
