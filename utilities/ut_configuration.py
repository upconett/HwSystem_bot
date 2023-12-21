import os.path
import json

from data_base.db_psql import PostgreSQL
from data_base.db_mongo import MongoDB

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
			return (MAIN_TOKEN, LOG_TOKEN, creator_id, api_hash, api_id, db_host, db_user, db_password, db_name)
		else:
			print("Missing some arguments in config.json!\n")
			first_configuration()
	else:
		print("It seems to be your first time launching the bot!\
			  \nLet's do some configuration...")
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
		else:
			print("DATA IS NOT VALID")
		return (MAIN_TOKEN, LOG_TOKEN, creator_id, api_hash, api_id, db_host, db_user, db_password, db_name)
		

def data_is_valid(data) -> bool:
	required_agrs = ['MAIN_TOKEN', 'LOG_TOKEN', 'creator_id', 'api_hash', 'api_id', 'db_host', 'db_user', 'db_password', 'db_name']
	# print(required_agrs,"\n",list(data.keys()))
	return list(data.keys()) == required_agrs


def validate_input(argument:str, message:str):
	output = input(message)
	if argument in ['MAIN_TOKEN', 'LOG_TOKEN']:
		while len(output) != 46:
			print('\nERROR > [TOKEN] should be 46 chars long and looking like this:\
		 			\n6933313572:dde6NYrts2jVfgpUdmEWynxliSdMnsVkfLM')
			output = input(message)
	elif argument == 'creator_id':
		while True:
			try: output = int(output)
			except ValueError:
				print('\nERROR > Your [id] should look like this: 3815494825')
				output = input(message)
				continue
			break
	elif argument == 'api_id':
		while True:
			try: output = int(output)
			except ValueError:
				print('\nERROR > [api_id] should look like this: 12306494')
				output = input(message)
				continue
			break
	elif argument == 'db_host':
		while not (output == 'localhost' or output.count('.') == 3):
			print('\nERROR > [db_host] has to look like this:\
		 		\n32.124.53.56 or be \'localhost\'')
			output = input(message)
	return output


def first_configuration():
	data = {}
	print("\n<1/5>\
		  \nBot [TOKEN] is required to work with TelegramAPI.\
		  \nYou can get it from: https://t.me/BotFather.")
	MAIN_TOKEN = validate_input('MAIN_TOKEN', 'Type in the [TOKEN] for your bot: ')
	print('\n<2/5>\
		  \nLogger is minimal bot that outputs runtime info of your main bot.\
		  \nGet another [TOKEN] for this one.')
	LOG_TOKEN = validate_input('LOG_TOKEN', 'Now type in the [TOKEN] for logger bot: ')
	print('\n<3/5>\
		  \nBots need to know who their creator is!\
		  \nYou need to provide your [user_id] (a sequence of numbers).\
		  \nYou can learn your [id] from: https://t.me/getmyid_bot.')
	creator_id = validate_input('creator_id', 'Type your [id] in here: ')
	print('\n<4/5>\
		  \nFor certain bot functions to work properly you need to provide [api_hash] and [api_id]\
		  \nTo get these follow the guide: https://core.telegram.org/api/obtaining_api_id')
	api_hash = input('Type [api_hash] first: ')
	api_id = validate_input('api_id', 'Here type [api_id]: ')
	print('\n<5/5>\
		  \nNow it\'s time to initialize databases!\
		  \nThe bot uses PostgreSQL and MongoDB so you need to set them running on your host.\
		  \nYou have to specify [db_host], [db_user], [db_password] and [db_name].\
		  \nRequired columns will be created automatically')
	db_host = validate_input('db_host', 'Type in [db_host] ("localhost" if db\'s are set on that machine): ')
	db_user = input('Now type in [db_user] (it has to be created in advance!): ')
	db_password = input('Type in [db_password] for the user: ')
	db_name = input('Type in [db_name] (that has to be created in advance!):')
	print('\nTrying to connect to PostgreSQL...')
	psql = PostgreSQL(db_host, db_user, db_password, db_name)
	print(f'Connection successfull!\
		  \nTables users, groups and chats required.')
	answer = str(input(f'Build tables for {db_name}? Existing tables will be removed! [Y/N]: ')).lower()
	while answer not in ['y','n']:
		answer = str(input("Print 'Y' or 'N' please: ")).lower()
	if answer == 'n':
		print('StartUp using created tables...')
	else:
		print('Building new tables...')
		psql.createTables()
		print('Tables built successfuly!')
	print('\nTrying to connect to MongoDB...')
	mndb = MongoDB(db_host, db_user, db_password, db_name)
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
	print('\nConfiguration complete!\
	   \nYou can change configuration any time in config.json\n')
