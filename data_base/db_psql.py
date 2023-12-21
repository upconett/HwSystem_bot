# <---------- Импорт сторонних функций ---------->
import psycopg2 as ps

from psycopg2.extensions import connection


# <---------- Импорт локальных функций ---------->
from utilities.ut_logger import ut_LogCreate


# <---------- Переменные ---------->
filename = 'db_psql.py'
__all__ = ['PostgreSQL', 'db_psql_InsertUser', 'db_psql_InsertChat', 'db_psql_InsertGroup']


# <---------- Основные классы ---------->
class PostgreSQL:
	"""
	Class for interact with PostgreSQL database.
	"""
	def __init__(self, host: str, database: str, user: str, password: str, port: int = 5432):
		"""
		Class constructor. Connection to PostgreSQL.
		:param host: IP-address to connect
		:param user: Username
		:param password:
		:param database: Database name
		:param port: Port to connect
		"""
		self.conn = ps.connect(host=host, port=port, dbname=database, user=user, password=password)
		self.conn.autocommit = True

    def createTables(self):
        """
        Tables creation. On first startup.
        """
        for table in ['users', 'groups', 'chats']:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(f'DROP DATABASE {table};')
            except:
                pass
            cursor.execute(
                f"CREATE TABLE public.users 
                (id int8 NOT NULL,
                username varchar NULL,
                full_name varchar NOT NULL,
                group_id int4 NULL,
                group_admin bool NULL DEFAULT false);"
                )




    async def select(self, table: str, what: str = '*', where: str = '', where_value: any = ''):
		"""
		Select line (lines) from table where column.
		:param table: Table (users, groups, chats)
		:param what: Select this from table
		:param where: Where this
		:param where_value: Equals this
		:return: Array with tuples if OK or False if not OK
		"""
		try:
			with self.conn.cursor() as cursor:
				if where != '':
					cursor.execute(f"SELECT {what} FROM {table} WHERE {where} = ?;", (where_value,))
				else:
					cursor.execute(f"SELECT {what} FROM {table};")
				return cursor.fetchall()
		except Exception as exception:
			print(f'FILENAME="{filename}"; FUNCTION="PostgreSQL.select"; CONTENT=""; EXCEPTION="{exception}";')
			return False

	async def update(self, table: str, what: str, what_value: any, where: str, where_value: any):
		"""
		Update column0 in line in table where column1.
		:param table: Table (users, groups, chats)
		:param what: Update this in table
		:param what_value: To this
		:param where: Where this
		:param where_value: Equals this
		:return: True if OK or False if not OK
		"""
		try:
			with self.conn.cursor() as cursor:
				cursor.execute(f"UPDATE {table} SET {what} = ? WHERE {where} = ?;", (what_value, where_value,))
			return True
		except Exception as exception:
			print(f'FILENAME="{filename}"; FUNCTION="PostgreSQL.update"; CONTENT=""; EXCEPTION="{exception}";')
			return False

	async def delete(self, table: str, where: str, where_value: any):
		"""
		Deleting line from table where column.
		:param table: Table (users, groups, chats)
		:param where: Delete line where this
		:param where_value: Equals this
		:return: True if OK or False if not OK
		"""
		try:
			with self.conn.cursor() as cursor:
				cursor.execute(f"DELETE FROM {table} WHERE {where} = ?;", (where_value,))
			return True
		except Exception as exception:
			print(f'FILENAME="{filename}"; FUNCTION="PostgreSQL.delete"; CONTENT=""; EXCEPTION="{exception}";')
			return False


# <---------- Основные функции ---------->
async def db_psql_InsertUser(db: connection, id: int, username: str, full_name: str):
	"""
	Insert new user in users table.
	:param db: Connect object
	:param id: Telegram id
	:param username: Telegram username
	:param full_name: Telegram full_name
	:return: True if OK or False if not OK
	"""
	try:
		with db.cursor() as cursor:
			cursor.execute(f'INSERT INTO users (id, username, full_name, group_id, group_admin) VALUES (?, ?, ?, ?, ?)', (id, username, full_name, None, False))
		return True
	except Exception as exception:
		await ut_LogCreate(
			id=00000000,
			filename=filename,
			function='db_psql_InsertUser',
			exception=exception,
			content=''
		)
		return False


async def db_psql_InsertGroup(db: connection, group_name: str, group_password: str, owner_id: int, default_lessons: dict = '', default_breaks: dict = ''):
	"""
	Insert new group in groups table.
	:param db: Connect object
	:param group_name:
	:param group_password:
	:param owner_id: Telegram id from owner
	:param default_lessons: Schedule {'weekday': {'0': 'lesson0',},}
	:param default_breaks: Schedule {'weekday': {'0': ['hh:MM - start', 'hhMM - end'],},}
	:return: True if OK or False if not OK
	"""
	try:
		with db.cursor() as cursor:
			cursor.execute(f'INSERT INTO users (group_id, group_name, group_password, owner_id, default_lessons, default_breaks) VALUES (?, ?, ?, ?, ?)', (None, group_name, group_password, owner_id, default_lessons, default_breaks))
		return True
	except Exception as exception:
		await ut_LogCreate(
			id=00000000,
			filename=filename,
			function='db_psql_InsertGroup',
			exception=exception,
			content=''
		)
		return False


async def db_psql_InsertChat(db: connection, id: int, title: str, group_id: int, notifications: bool):
	"""
	Insert new chat in chats table.
	:param db: Connect object
	:param id: Telegram chat id
	:param title: Telegram chat title
	:param group_id: Group id
	:param notifications: Notification for now
	:return: True if OK or False if not OK
	"""
	try:
		with db.cursor() as cursor:
			cursor.execute(f'INSERT INTO chats (id, title, notifications, group_id) VALUES (?, ?, ?, ?)', (id, title, notifications, group_id))
		return True
	except Exception as exception:
		await ut_LogCreate(
			id=00000000,
			filename=filename,
			function='db_psql_InsertChat',
			exception=exception,
			content=''
		)
		return False
