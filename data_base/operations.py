# <---------- Local modules ---------->
from messages.ms_regular import boolToRussian
from create_bot import psql


# <---------- Python modules ---------->
from datetime import datetime


# <---------- Variables ---------->
filename = 'operations.py'
__all__ = ['insertUser', 'insertChat', 'userData', 'chatData', 'groupData', 'insertGroup', 'getMainSchedule', 'setMainSchedule']


# <---------- Interoperability with PostgreSQL ---------->
async def insertUser(id: int, username: str, full_name: str):
	"""
	Insert new user in users table.
	:param id: Telegram id
	:param username: Telegram username
	:param full_name: Telegram full_name
	:return: True if OK or False if not OK
	"""
	try:
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with psql.conn.cursor() as cursor:
			cursor.execute(f'INSERT INTO users (id, username, full_name, group_id, group_admin, date) VALUES (%s, %s, %s, %s, %s, %s)', (id, username, full_name, None, False, date))
		return True
	except Exception as exception:
		print(f'FILENAME="{filename}"; FUNCTION="db_psql_InsertUser"; CONTENT=""; EXCEPTION="{exception}";')
		return False


async def insertGroup(group_name: str, group_password: str, owner_id: int, default_lessons: dict = '', default_breaks: dict = ''):
	"""
	Insert new group in groups table.
	:param group_name:
	:param group_password:
	:param owner_id: Telegram id from owner
	:param default_lessons: Schedule {'weekday': {'0': 'lesson0',},}
	:param default_breaks: Schedule {'weekday': {'0': ['hh:MM - start', 'hhMM - end'],},}
	:return: True if OK or False if not OK
	"""
	try:
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with psql.conn.cursor() as cursor:
			cursor.execute(f'INSERT INTO users (group_id, group_name, group_password, group_link, owner_id, default_lessons, default_breaks, date) VALUES (%s, %s, %s, %s, %s, %s)', (None, group_name, group_password, None, owner_id, default_lessons, default_breaks, date))
		return True
	except Exception as exception:
		print(f'FILENAME="{filename}"; FUNCTION="db_psql_InsertGroup"; CONTENT=""; EXCEPTION="{exception}";')
		return False


async def insertChat(id: int, title: str, group_id: int, notifications: bool):
	"""
	Insert new chat in chats table.
	:param id: Telegram chat id
	:param title: Telegram chat title
	:param group_id: Group id
	:param notifications: Notification for now
	:return: True if OK or False if not OK
	"""
	try:
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with psql.conn.cursor() as cursor:
			cursor.execute(f'INSERT INTO chats (id, title, notifications, group_id, date) VALUES (%s, %s, %s, %s, %s)', (id, title, notifications, group_id, date))
		return True
	except Exception as exception:
		print(f'FILENAME="{filename}"; FUNCTION="db_psql_InsertChat"; CONTENT=""; EXCEPTION="{exception}";')
		return False


async def userData(id: int, formatted: bool = False):
	"""
	Return data about user formatted or not.
	:param id: Telegram ID
	:param formatted: Dictionary for code or str for output
	:return: Dictionary if formatted False or string if formatted True
	"""
	response = (await psql.select(
		table='users',
		what='*',
		where='id',
		where_value=id
	))
	if not formatted:
		if not response:
			response = [id, '', '', '', '', '']
		else:
			response = [response[0][0], response[0][1], response[0][2], response[0][3], response[0][4], response[0][5]]
			response[5] = response[5].strftime('%Y-%m-%d %H:%M:%S')
		data = {
			'id': response[0],
			'username': response[1],
			'full_name': response[2],
			'group_id': response[3],
			'group_admin': response[4],
			'date': response[5]
		}
	else:
		if not response:
			data = (
				f'Пользователь не зарегистрирован в боте!\n'
				f' Telegram ID: {id}'
			)
		else:
			response = response[0]
			data = (
				f'Зарегистрирован: {response[5].strftime("%Y-%m-%d %H:%M:%S")}\n'
				f' Telegram ID: {response[0]}\n'
				f' Аккаунт: {response[1]}\n'
				f' Полное имя: {response[2]}\n'
				f' ID группы: {response[3]}\n'
				f' Является админом группы: {boolToRussian[response[4]]}'
			)
	return data


async def chatData(id: int, formatted: bool = False):
	"""
	Return data about chat formatted or not.
	:param id: Telegram chat ID
	:param formatted: Dictionary for code or str for output
	:return: Dictionary if formatted False or string if formatted True
	"""
	response = (await psql.select(
		table='chats',
		what='*',
		where='id',
		where_value=id
	))
	if not formatted:
		if not response:
			response = [id, '', '', '', '']
		else:
			response = [response[0][0], response[0][1], response[0][2], response[0][3], response[0][4]]
			response[4] = response[4].strftime('%Y-%m-%d %H:%M:%S')
		data = {
			'id': response[0],
			'title': response[1],
			'notifications': response[2],
			'group_id': response[3],
			'date': response[4]
		}
	else:
		if not response:
			data = (
				f'Чат не зарегистрирован в боте!\n'
				f' Telegram chat ID: {id}'
			)
		else:
			response = response[0]
			data = (
				f'Зарегистрирован: {response[4].strftime("%Y-%m-%d %H:%M:%S")}\n'
				f' Telegram chat ID: {response[0]}\n'
				f' Название: {response[1]}\n'
				f' ID группы: {response[3]}\n'
				f' Уведомления: {boolToRussian[response[2]]}'
			)
	return data


async def groupData(group_id: int, formatted: bool = False):
	"""
	Return data about group formatted or not.
	:param group_id: Group ID
	:param formatted: Dictionary for code or str for output
	:return: Dictionary if formatted False or string if formatted True
	"""
	response = (await psql.select(
		table='groups',
		what='*',
		where='group_id',
		where_value=group_id
	))
	if not formatted:
		if not response:
			response = [group_id, '', '', '', '']
		else:
			response = [response[0][0], response[0][1], response[0][3], response[0][4], response[0][7]]
			response[4] = response[4].strftime('%Y-%m-%d %H:%M:%S')
		data = {
			'group_id': response[0],
			'group_name': response[1],
			'group_link': response[2],
			'owner_id': response[3],
			'date': response[4]
		}
	else:
		if not response:
			data = (
				f'Группа не зарегистрирован в боте!\n'
				f' Group ID: {group_id}'
			)
		else:
			response = response[0]
			data = (
				f'Зарегистрирована: {response[7].strftime("%Y-%m-%d %H:%M:%S")}\n'
				f' Group ID: {response[0]}\n'
				f' Название: {response[1]}\n'
				f' Telegram ID владельца: {response[4]}\n'
				f' Ссылка на вступление: {response[3]}'
			)
	return data


async def getMainSchedule(id: int):
	"""
	Get default schedule from database.
	:param id: Telegram ID of user
	:return:
	"""
	try:
		group_id = (await psql.select(
			table='users',
			what='group_id',
			where='id',
			where_value=id
		))[0]
		schedule = (await psql.select(
			table='groups',
			what='default_lessons',
			where='group_id',
			where_value=group_id
		))[0]
		return schedule
	except Exception as exception:
		print(f'FILENAME="{filename}"; FUNCTION="db_psql_InsertChat"; CONTENT=""; EXCEPTION="{exception}";')
		return False


async def setMainSchedule(id: int, data: dict):
	"""
	Set default schedule in database.
	:param id: Telegram ID of user.
	:param data: Schedule
	:return:
	"""
	try:
		group_id = (await psql.select(
			table='users',
			what='group_id',
			where='id',
			where_value=id
		))[0]
		update = await psql.update(
			table='groups',
			what='default_lessons',
			what_value=data,
			where='group_id',
			where_value=group_id
		)
		return update
	except Exception as exception:
		print(f'FILENAME="{filename}"; FUNCTION="db_psql_InsertChat"; CONTENT=""; EXCEPTION="{exception}";')
		return False
