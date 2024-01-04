# <---------- Импорт сторонних функций ---------->
import psycopg2 as ps
import json


# <---------- Переменные ---------->
filename = 'db_psql.py'
__all__ = ['PostgreSQL']


# <---------- Основные классы ---------->
class PostgreSQL:
	"""
	Class for interact with PostgreSQL database.
	"""
	def __init__(self, host: str, user: str, password: str, database: str, port: int = 5432):
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
					cursor.execute(f'DROP TABLE {table};')
			except Exception as exception:
				print(f'CANNOT DROP TABLE with exception "{exception}"')
		with self.conn.cursor() as cursor:
			cursor.execute(r"""CREATE TABLE users
			(id int8 NOT NULL,
			username varchar NULL,
			full_name varchar NOT NULL,
			group_id int4 NULL,
			group_admin bool NULL DEFAULT false,
			date timestamp NOT NULL);""")
		with self.conn.cursor() as cursor:
			cursor.execute(r"""CREATE TABLE groups (
			group_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
			group_name varchar NOT NULL,
			group_password varchar NOT NULL,
			group_link varchar NULL,
			owner_id int8 NOT NULL,
			default_lessons json NULL DEFAULT '{}'::json,
			default_breaks json NULL DEFAULT '{}'::json,
			date timestamp NOT NULL);""")
		with self.conn.cursor() as cursor:
			cursor.execute(r"""CREATE TABLE chats (
			id int8 NOT NULL,
			title varchar NOT NULL,
			notifications bool NOT NULL,
			group_id int4 NOT NULL,
			date timestamp NOT NULL);""")

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
					cursor.execute(f"SELECT {what} FROM {table} WHERE {where} = %s", (where_value,))
				else:
					cursor.execute(f"SELECT {what} FROM {table}")
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
			if type(what_value) is dict or what_value is list:
				what_value = json.dumps(what_value, ensure_ascii=False)
			with self.conn.cursor() as cursor:
				cursor.execute(f"UPDATE {table} SET {what} = %s WHERE {where} = %s", (what_value, where_value))
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
				cursor.execute(f"DELETE FROM {table} WHERE {where} = %s", (where_value,))
			return True
		except Exception as exception:
			print(f'FILENAME="{filename}"; FUNCTION="PostgreSQL.delete"; CONTENT=""; EXCEPTION="{exception}";')
			return False


	async def close(self):
		self.conn.close()
		print('PostgreSQL connection closed')