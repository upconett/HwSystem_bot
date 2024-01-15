# <---------- Local modules ---------->
from messages.ms_regular import boolToRussian
from create_bot import psql
from create_bot import mndb
from exceptions.ex_handlers import SundayException, NoLessonAtWeekday

# <---------- Python modules ---------->
import json
from datetime import datetime, timedelta


# <---------- Variables ---------->
filename = 'operations.py'
__all__ = ['insertUser', 'insertChat', 'userData', 'chatData', 'groupData', 'insertGroup', 'getMainSchedule', 'setMainSchedule']


# <---------- Utility ---------->
def dateToday(date: datetime = None) -> datetime:
	"""
	Returns datetime object with the time set to zero.
	"""
	if date:
		return date.replace(
			hour=0,
			minute=0,
			second=0,
			microsecond=0
		)
	else:
		return datetime.now().replace(
			hour=0,
			minute=0,
			second=0,
			microsecond=0
		)


# <---------- Interoperability with PostgreSQL ---------->
async def insertUser(id: int, username: str, full_name: str):
	"""
	Insert new user in users table.\n
	---
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


async def insertGroup(group_name: str, group_password: str, owner_id: int, default_lessons: str = '{}', default_breaks: str = '{}'):
	"""
	Insert new group in groups table.\n
	---
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
			cursor.execute(f'INSERT INTO groups (group_name, group_password, group_link, owner_id, default_lessons, default_breaks, date) VALUES (%s, %s, %s, %s, %s, %s, %s)', (group_name, group_password, None, owner_id, default_lessons, default_breaks, date))
		return True
	except Exception as exception:
		print(f'FILENAME="{filename}"; FUNCTION="db_psql_InsertGroup"; CONTENT=""; EXCEPTION="{exception}";')
		return False


async def insertChat(id: int, title: str, group_id: int, notifications: bool):
	"""
	Insert new chat in chats table.\n
	---
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


async def userData(id: int, formatted: bool = False) -> dict:
	"""
	Return data about user formatted or not.\n
	---
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
			response = [id, None, None, None, None, None]
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


async def chatData(id: int, formatted: bool = False) -> dict:
	"""
	Return data about chat formatted or not.\n
	---
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


async def groupData(group_id: int, formatted: bool = False) -> dict:
	"""
	Return data about group formatted or not.\n
	---
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


async def getMainSchedule(id: int) -> dict:
	"""
	Get default schedule from database.\n
	---
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
		if schedule:
			return schedule[0]
		else:
			return None
	except Exception as exception:
		print(f'FILENAME="{filename}"; FUNCTION="getMainSchedule"; CONTENT=""; EXCEPTION="{exception}";')
		return False


async def setMainSchedule(id: int, data: dict):
	"""
	Set default schedule in database.\n
	---
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


async def findNextLesson(id: int, subject: str, date: datetime = None, weekday: str = None) -> dict[datetime, int, int]:
	"""
	Finds next lesson in MainSchedule.\n
	---
	:param id: User id
	:param subject: Subject to find
	:param date_str: Date when to seek
	:return: Dict with date, weekday and lesson
	"""
	date_now = datetime.now()
	result = {
		'date': None,
		'lesson': None
	}
	schedule = await getMainSchedule(id)
	weekdays = schedule.keys()
	if date:
		wd = date.weekday()
		if wd == 6:
			raise SundayException
		day = list(weekdays)[wd]
		for lesson in schedule[day]:
			if schedule[day][lesson] == subject:
				result['date'] = dateToday(date)
				result['lesson'] = int(lesson)
				return result
		else:
			raise NoLessonAtWeekday(day, subject)
	if weekday:
		weekday = weekday.capitalize()
		wd = list(weekdays).index(weekday)
		wd_now = datetime.now().weekday()
		if wd == wd_now:
			date = datetime.now()
		else:
			if wd > wd_now:
				date = datetime.now() + timedelta(days = (wd - wd_now))
			else:
				date = datetime.now() + timedelta(days = ((6 - wd_now) + wd)+1)
		for lesson in schedule[weekday]:
			if schedule[weekday][lesson] == subject:
				result['date'] = dateToday(date)
				result['lesson'] = int(lesson)
				return result
		else:
			raise NoLessonAtWeekday(weekday, subject)
	else:
		date = date_now + timedelta(days = 1)
		wd = date.weekday()
		if wd == 6:
			wd == 0
		for i in range(2):
			for day in list(weekdays)[wd:]:
				for lesson in schedule[day]:
					if schedule[day][lesson] == subject:
						result['date'] = dateToday(date)
						result['lesson'] = int(lesson)
						return result
				date = date + timedelta(days = 1)
			date = date + timedelta(days = 1)
			wd = date.weekday()
	return result


def generateMongoRecord(date: datetime, schedule: dict, breaks: dict = None, subject: str = None, task: str = None, photos: list = None) -> dict:
	"""
	Generates dict file with schedule and tasks info that will be stored in MongoDB.\n
	---
	:param date: Date as a key value.
	:param schedule: Main schedule set in group.
	:param breaks: Breaks schedule set in group.
	:param subject: Subject on which to store task. (Optional)
	:param task: Task that will be written to subject. (Optional)
	:param photos: Photos that will be attached to subject. (Optional)
	:return:
	"""
	tasks = {}
	for lesson in schedule:
		if schedule[lesson] is None:
			continue
		tasks[schedule[lesson]] = {
			'task': None, 
			'photos': None
		}
	if subject:
		tasks[subject] = {
			'task': task,
			'photos': photos
		}
	result = {
		'date': date,
		'schedule': schedule,
		'breaks': breaks,
		'tasks': tasks
	}
	return result


async def getHomework(id: int, date: datetime = None, subject: str = None) -> dict:
	"""
	Returns homework for specified date or subject.\n
	If heither given, return all tasks for tomorrow.\n
	---
	:param id: User id.
	:param date: Date on which to look for data.
	:param subject: Subject that we are looking for.
	:return:
	"""
	group_id = (await psql.select(
		'users',
		'group_id',
		'id', id
	))[0][0]
	group_name = (await psql.select(
		'groups',
		'group_name',
		'group_id', group_id
	))[0][0]
	if not date:
		date = datetime.now() + timedelta(hours=12)
	collections = mndb.db.list_collection_names()
	if group_name not in collections:
		raise Exception(f'MongoDB has no collection named {group_name}')
	coll = mndb.db.get_collection(group_name)
	record = coll.find_one({'date': dateToday(date)})
	if not record: return record
	homework = record['tasks']
	if subject:
		return homework[subject]
	return homework


async def setHomework(id: int, date: datetime, subject: str, task: str = None, photos: list = None) -> bool:
	"""
	Sets task on subject provided.\n
	Creates new MongoDB document if there is no hw for given date.\n
	---
	:param id: User id.
	:param date: Date on which to store data.
	:param subject: Subject on which to set task.
	:param task: Task to be set.
	:param photos: Photos to be attached.
	:return:
	"""
	group_id = (await psql.select(
		'users',
		'group_id',
		'id', id
	))[0][0]
	group_name = (await psql.select(
		'groups',
		'group_name',
		'group_id', group_id
	))[0][0]
	collections = mndb.db.list_collection_names()
	if group_name not in collections:
		raise Exception(f'MongoDB has no collection named {group_name}')
	coll = mndb.db.get_collection(group_name)
	record = coll.find_one({'date': dateToday(date)})
	if not record:
		schedule = await getMainSchedule(id)
		weekday = list(schedule.keys())[date.weekday()]
		coll.insert_one(generateMongoRecord(
			date=dateToday(date),
			schedule=schedule[weekday],
			subject=subject,
			task=task,
			photos=photos
		))
	else:
		modified = record
		modified['tasks'][subject] = {
			'task': task,
			'photos': photos
		}
		coll.replace_one(
			filter={'date': record['date']},
			replacement=modified
		)
	return True


async def closestDates(id: int, date: datetime) -> tuple[datetime, datetime]:
	"""
	Checks if there is any homework before and after given date.\n
	---
	:param id: _User id.
	:param date: Date across which to seak.
	:return:
	"""
	next_date, prev_date = (None, None)
	group_id = (await psql.select(
		'users',
		'group_id',
		'id', id
	))[0][0]
	group_name = (await psql.select(
		'groups',
		'group_name',
		'group_id', group_id
	))[0][0]
	collections = mndb.db.list_collection_names()
	if group_name not in collections:
		raise Exception(f'MongoDB has no collection named {group_name}')
	coll = mndb.db.get_collection(group_name)
	try:
		cursor = coll.find({'date': {'$gt': dateToday(date)}})
		next_date = min(cursor.distinct('date'))
	except: pass
	try:
		cursor = coll.find({'date': {'$lt': dateToday(date)}})
		prev_date = max(cursor.distinct('date'))
	except: pass
	return (next_date, prev_date)