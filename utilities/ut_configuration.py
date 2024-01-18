# <---------- Python modules ---------->
import os.path
import json


# <---------- Local modules ---------->
from data_base.db_psql import PostgreSQL
from data_base.db_mongo import MongoDB

from messages import ms_configuration


# <---------- Configurator ---------->
def startupConfiguration():
	exception_data = (0, 0, 0, 0, 0, 0, 0, 0, 0)
	if os.path.isfile('config.json'):
		with open('config.json') as file:
			data = json.load(file)
		if data_is_valid(data):
			MAIN_TOKEN = data["MAIN_TOKEN"]
			LOG_TOKEN = data["LOG_TOKEN"]
			creators = data["creators"]
			api_hash = data["api_hash"]
			api_id = data["api_id"]
			db_host = data["db_host"]
			db_user = data["db_user"]
			db_password = data["db_password"]
			db_name = data["db_name"]
			return MAIN_TOKEN, LOG_TOKEN, creators, api_hash, api_id, db_host, db_user, db_password, db_name
		else:
			print("Missing some arguments in config.json!\n")
			if first_configuration() == -1:
				print('Configuration Error!')
				return exception_data
		if data_is_valid(data):
			MAIN_TOKEN = data["MAIN_TOKEN"]
			LOG_TOKEN = data["LOG_TOKEN"]
			creators = data["creators"]
			api_hash = data["api_hash"]
			api_id = data["api_id"]
			db_host = data["db_host"]
			db_user = data["db_user"]
			db_password = data["db_password"]
			db_name = data["db_name"]
			return MAIN_TOKEN, LOG_TOKEN, creators, api_hash, api_id, db_host, db_user, db_password, db_name
		else:
			return exception_data
	else:
		print(
			"It seems to be your first time launching the bot!\n"
			"Let's do some configuration..."
		)
		if first_configuration() == -1:
			print('Configuration Error!')
			return exception_data
		with open('config.json', 'r') as file:
			data = json.load(file)
		if data_is_valid(data):
			MAIN_TOKEN = data["MAIN_TOKEN"]
			LOG_TOKEN = data["LOG_TOKEN"]
			creators = data["creators"]
			api_hash = data["api_hash"]
			api_id = data["api_id"]
			db_host = data["db_host"]
			db_user = data["db_user"]
			db_password = data["db_password"]
			db_name = data["db_name"]
			return MAIN_TOKEN, LOG_TOKEN, creators, api_hash, api_id, db_host, db_user, db_password, db_name
		else:
			return exception_data
		

def data_is_valid(data) -> bool:
	required_args = ['MAIN_TOKEN', 'LOG_TOKEN', 'creators', 'api_hash', 'api_id', 'db_host', 'db_user', 'db_password', 'db_name']
	return list(data.keys()) == required_args


def validate_input(argument: str, message: str):
	output = input(message)
	if argument in ['MAIN_TOKEN', 'LOG_TOKEN']:
		while len(output) != 46:
			print(ms_configuration.errorMainToken)
			output = input(message)
	elif argument == 'creators':
		while True:
			try:
				output = int(output)
			except ValueError:
				print(ms_configuration.errorCreators)
				output = input(message)
				continue
			break
	elif argument == 'api_id':
		while True:
			try:
				output = int(output)
			except ValueError:
				print(ms_configuration.errorApiId)
				output = input(message)
				continue
			break
	elif argument == 'db_host':
		while not (output == 'localhost' or output.count('.') == 3):
			print(ms_configuration.errorDBHost)
			output = input(message)
	return output


def first_configuration():
	print(ms_configuration.mainToken)
	MAIN_TOKEN = validate_input('MAIN_TOKEN', 'Type in the [TOKEN] for your bot: ')
	
	print(ms_configuration.logToken)
	LOG_TOKEN = validate_input('LOG_TOKEN', 'Now type in the [TOKEN] for logger bot: ')

	print(ms_configuration.creators)
	number = int(input('Type in the number of creators: '))
	creators = []
	for i in range(number):
		creators.append(validate_input('creators', f'Type in {i+1} creator [id]: '))

	print(ms_configuration.apiHashId)
	api_hash = input('Type [api_hash] first: ')
	api_id = validate_input('api_id', 'Here type [api_id]: ')

	print(ms_configuration.DBProperties)
	db_host = validate_input('db_host', "Type in [db_host] ('localhost' if db's are set on that machine): ")
	db_user = input('Now type in [db_user] (it has to be created in advance!): ')
	db_password = input('Type in [db_password] for the user: ')
	db_name = input('Type in [db_name] (that has to be created in advance!): ')
	print('\nTrying to connect to PostgreSQL...')
	try:
		psql = PostgreSQL(db_host, db_user, db_password, db_name)
	except Exception as ex:
		print(
			'Connection Error!\n'
			f'Exception: {ex}'
			)
		return -1
	print(
		'Connection successful!\n'
		'Tables users, groups and chats required.'
	)
	answer = str(input(f'Build tables for {db_name}? Existing tables will be removed! [Y/N]: ')).lower()
	while answer not in ['y', 'n']:
		answer = str(input("Print 'Y' or 'N' please: ")).lower()
	if answer == 'n':
		print('StartUp using created tables...')
	else:
		print('Building new tables...')
		psql.createTables()
		print('Tables built successfully!')
	print('\nTrying to connect to MongoDB...')
	try:
		MongoDB(db_host, db_user, db_password, db_name)
	except Exception as ex:
		print(
			'Connection Error!\n'
			f'Exception: {ex}'
			)
		return -1
	print('Connection successful!')
	data = {
		'MAIN_TOKEN': MAIN_TOKEN,
		'LOG_TOKEN': LOG_TOKEN,
		'creators': creators,
		'api_hash': api_hash,
		'api_id': api_id,
		'db_host': db_host,
		'db_user': db_user,
		'db_password': db_password,
		'db_name': db_name
		}
	with open('config.json', 'w') as file:
		json.dump(data, file, indent=2)
	print(
		'\nConfiguration complete!\n'
		'You can change configuration any time in config.json\n'
	)
