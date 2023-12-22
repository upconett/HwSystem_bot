# <---------- Импорт сторонних функций ---------->
import os.path
import json


# <---------- Импорт локальных функций ---------->
from data_base.db_psql import PostgreSQL


# <---------- Основные функции ---------->
def ut_startupConfiguration():
	if os.path.isfile('config.json'):
		with open('config.json') as file:
			data = json.load(file)
		if data_is_valid(data):
			MAIN_TOKEN = data["MAIN_TOKEN"]
			LOG_TOKEN = data["LOG_TOKEN"]
			creator_id = data["creator_id"]
			api_hash = data["api_hash"]
			api_id = data["api_id"]
			db_host = data["db_host"]
			db_user = data["db_user"]
			db_password = data["db_password"]
			db_name = data["db_name"]
			return MAIN_TOKEN, LOG_TOKEN, creator_id, api_hash, api_id, db_host, db_user, db_password, db_name
		else:
			print("Missing some arguments in config.json!\n")
			first_configuration()
	else:
		print(
			"It seems to be your first time launching the bot!\n"
			"Let's do some configuration..."
		)
		first_configuration()
		with open('config.json', 'r') as file:
			data = json.load(file)
		if data_is_valid(data):
			MAIN_TOKEN = data["MAIN_TOKEN"]
			LOG_TOKEN = data["LOG_TOKEN"]
			creator_id = data["creator_id"]
			api_hash = data["api_hash"]
			api_id = data["api_id"]
			db_host = data["db_host"]
			db_user = data["db_user"]
			db_password = data["db_password"]
			db_name = data["db_name"]
			return MAIN_TOKEN, LOG_TOKEN, creator_id, api_hash, api_id, db_host, db_user, db_password, db_name
		else:
			print("DATA IS NOT VALID")
		

def data_is_valid(data) -> bool:
	required_args = ['MAIN_TOKEN', 'LOG_TOKEN', 'creator_id', 'api_hash', 'api_id', 'db_host', 'db_user', 'db_password', 'db_name']
	return list(data.keys()) == required_args


def validate_input(argument: str, message: str):
	output = input(message)
	if argument in ['MAIN_TOKEN', 'LOG_TOKEN']:
		while len(output) != 46:
			print(
				'\nERROR > [TOKEN] should be 46 chars long and looking like this:\n'
				'6933313572:dde6NYrts2jVfgpUdmEWynxliSdMnsVkfLM'
			)
			output = input(message)
	elif argument == 'creator_id':
		while True:
			try:
				output = int(output)
			except ValueError:
				print('\nERROR > Your [id] should look like this: 3815494825')
				output = input(message)
				continue
			break
	elif argument == 'api_id':
		while True:
			try:
				output = int(output)
			except ValueError:
				print('\nERROR > [api_id] should look like this: 12306494')
				output = input(message)
				continue
			break
	elif argument == 'db_host':
		while not (output == 'localhost' or output.count('.') == 3):
			print(
				'\nERROR > [db_host] has to look like this:\n'
				'32.124.53.56 or be "localhost"'
			)
			output = input(message)
	return output


def first_configuration():
	print(
		"\n<1/5>\n"
		"Bot [TOKEN] is required to work with TelegramAPI.\n"
		"You can get it from: https://t.me/BotFather."
	)
	MAIN_TOKEN = validate_input('MAIN_TOKEN', 'Type in the [TOKEN] for your bot: ')
	print(
		'\n<2/5>\n'
		'Logger is minimal bot that outputs runtime info of your main bot.\n'
		'Get another [TOKEN] for this one.'
	)
	LOG_TOKEN = validate_input('LOG_TOKEN', 'Now type in the [TOKEN] for logger bot: ')
	print(
		'\n<3/5>\n'
		'Bots need to know who their creator is!\n'
		'You need to provide your [user_id] (a sequence of numbers).\n'
		'You can learn your [id] from: https://t.me/getmyid_bot.'
	)
	creator_id = validate_input('creator_id', 'Type your [id] in here: ')
	print(
		'\n<4/5>\n'
		'For certain bot functions to work properly you need to provide [api_hash] and [api_id]\n'
		'To get these follow the guide: https://core.telegram.org/api/obtaining_api_id'
	)
	api_hash = input('Type [api_hash] first: ')
	api_id = validate_input('api_id', 'Here type [api_id]: ')
	print(
		"\n<5/5>\n"
		"Now it's time to initialize databases!\n"
		"The bot uses PostgreSQL and MongoDB so you need to set them running on your host.\n"
		"You have to specify [db_host], [db_user], [db_password] and [db_name].\n"
		"Required columns will be created automatically"
	)
	db_host = validate_input('db_host', "Type in [db_host] ('localhost' if db's are set on that machine): ")
	db_user = input('Now type in [db_user] (it has to be created in advance!): ')
	db_password = input('Type in [db_password] for the user: ')
	db_name = input('Type in [db_name] (that has to be created in advance!): ')
	print('\nTrying to connect to PostgreSQL...')
	psql = PostgreSQL(db_host, db_user, db_password, db_name)
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
	print(f'Connection successful!')
	data = {
		'MAIN_TOKEN': MAIN_TOKEN,
		'LOG_TOKEN': LOG_TOKEN,
		'creator_id': creator_id,
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
