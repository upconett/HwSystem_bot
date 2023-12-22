# <---------- Импорт сторонних функций ---------->
from pymongo.mongo_client import MongoClient


# <---------- Основные классы ---------->
class MongoDB:
	def __init__(self, host: str, user: str, password: str, database: str, port: int = 27017):
		"""
		Class constructor, connecting to MongoDB Server
		- mongodb://bot:apropos019KOI@es53:27017/Homeworker?authMechanism=SCRAM-SHA-256
		:param host: IP-address to connect
		:param user: Username
		:param password:
		:param database: Database name
		:param port: Port to connect
		"""
		self.db = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/{database}?authMechanism=SCRAM-SHA-256")
		self.db = self.db.get_database(database)
		print('MongoDB started OK!')
