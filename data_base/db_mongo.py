# <---------- Python modules ---------->
from pymongo.mongo_client import MongoClient


# <---------- Connection class ---------->
class MongoDB:
	"""
	Class for interact with MongoDB database.
	"""
	def __init__(self, host: str, user: str, password: str, database: str, port: int = 27017):
		"""
		Class constructor, connecting to MongoDB Server.
		Link: mongodb://bot:apropos019KOI@es53:27017/Homeworker?authMechanism=SCRAM-SHA-256
		:param host: IP-address to connect
		:param user: Username
		:param password:
		:param database: Database name
		:param port: Port to connect
		"""
		self.connectionString = f'mongodb://{user}:{password}@{host}:{port}/{database}?authMechanism=SCRAM-SHA-256'
		self.database: str = database
		self.conn = MongoClient(self.connectionString)
		self.db = self.conn.get_database(self.database)


	async def reconnect(self):
		self.conn = MongoClient(self.connectionString)
		self.db = self.conn.get_database(self.database)


	async def close(self):
		self.conn.close()
		print('MongoDB connection closed.')
