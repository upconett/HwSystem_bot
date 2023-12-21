# <---------- Импорт локальных функций ---------->
from data_base.db_mongo import MongoDB
from data_base.db_psql import PostgreSQL
from config import db_host, db_name, db_user, db_password
from messages.ms_regular import msreg_TrueOrFalseToRussian


# <---------- Переменные ---------->
psql = None
mndb = None
filename = 'operation.py'


# <---------- Вспомогательные функции ---------->
def db_PsqlStart():
	"""
	Start connection with PostgreSQL database. Use only once!
	:return: True if OK or False if not OK
	"""
	global psql
	psql = PostgreSQL(host=db_host, user=db_user, password=db_password, database=db_name)
	return True


def db_MongoDbStart():
	"""
	Start connection with PostgreSQL database. Use only once!
	:return: True if OK or False if not OK
	"""
	global mndb
	mndb = MongoDB(host=db_host, user=db_user, password=db_password, database=db_name)
	return True


# <---------- Основные функции ---------->
async def db_psql_UserData(id: int, formatted: bool = False):
	"""
	Return data about user formatted or not.
	:param id: Telegram ID
	:param formatted: Dictionary for code or str for output
	:return: Dictionary if formatted False or string if formatted True
	"""
	response = (await PostgreSQL.select(
		self=psql,
		table='users',
		what='*',
		where='id',
		where_value=id
	))[0]
	if not formatted:
		if not response:
			response = [id, '', '', '', '', '']
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
			data = (
				f'Зарегистрирован: {response[5]}\n'
				f' Telegram ID: {response[0]}\n'
				f' Аккаунт: {response[1]}\n'
				f' Полное имя: {response[2]}\n'
				f' ID группы: {response[3]}\n'
				f' Является админом группы: {msreg_TrueOrFalseToRussian[response[4]]}'
			)
	return data
