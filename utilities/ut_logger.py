# <---------- Python modules ---------->
import logging

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


# <---------- Local modules ---------->
from data_base import operations


# <---------- Variables ---------->
logger = None


# <---------- Interoperability with logger ---------->
def start_logger():
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


async def create_log(id: int, filename: str, function: str, exception, content: str, chat_id: int = None):
	"""
	Creating new log.
	:param id: Telegram ID of user
	:param filename: File name
	:param function: Function name
	:param exception: Exception or str object
	:param content:
	:param chat_id: Telegram ID of chat
	:return:
	"""
	if id == 00000000:
		user = {
			'username': 'bot',
		}
	else:
		user = await operations.userData(id=id)
	if chat_id:
		chat = await operations.chatData(id=chat_id)
		if chat['group_id']:
			group = await operations.groupData(group_id=chat['group_id'])
		else:
			group = {}
		log_message = f'USER={user}; CHAT={chat}; GROUP={group}; FILENAME="{filename}"; FUNCTION="{function}"; CONTENT="{content}"; EXCEPTION="{exception}";'
	else:
		log_message = f'USER={user}; FILENAME="{filename}"; FUNCTION="{function}"; CONTENT="{content}"; EXCEPTION="{exception}";'
	date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(f'DATE="{date}"; {log_message}')
	logger.info(log_message)
