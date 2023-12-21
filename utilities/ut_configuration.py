import os.path
import json

def ut_startupConfiguration():
    if os.path.isfile('config.json'):
        with open('config.json') as file:
            data = json.load(file)
        if data_is_valid(data):
            MAIN_TOKEN = data["MAIN_TOKEN"]
            LOG_TOKEN = data["LOG_TOKEN"]
            creator_id = data["creator_id"]
            db_host = data["db_host"]
            db_user = data["db_user"]
            db_password = data["db_password"]
            db_name = data["db_name"]
            return (MAIN_TOKEN, LOG_TOKEN, creator_id, db_host, db_user, db_password, db_name)
        else:
            print("Missing some arguments in config.json!\n")
            first_configuration()
    else:
        print("It seems to be your first time launching the bot!\
              \nLet's do some configuration...")
        first_configuration()


def data_is_valid(data) -> bool:
    required_agrs = ['MAIN_TOKEN', 'LOG_TOKEN', 'creator_id', 'db_host', 'db_user', 'db_password', 'db_name']
    return list(data.keys()) == required_agrs


def first_configuration():
    print("\n<1/7>\
          \nBot [TOKEN] is required to work with TelegramAPI.\
          \nYou can get it from: https://t.me/BotFather.")
    MAIN_TOKEN = input('Type in the [TOKEN] for your bot: ')
    print('\n<2/7>\
          \nLogger is minimal bot that outputs runtime info of your main bot.\
          \nGet another [TOKEN] for this one.')
    LOG_TOKEN = input('Now type in the [TOKEN] for logger bot: ')
    print('\n<3/7>\
          \nBots need to know who their creator is!\
          \nYou need to provide your [user_id] (a sequence of numbers).\
          \nYou can learn your [id] from: https://t.me/getmyid_bot.')
    owner_id = input('Type your [id] in here: ')
    print('\n<4/7>\
          \nFor certain bot functions to work properly you need to provide [api_hash] and [api_id]\
          \nTo get these follow the guide: https://core.telegram.org/api/obtaining_api_id')
    api_hash = input('Type [api_hash] first: ')
    api_id = input('Here type [api_id]: ')
    print('\n<5/7>\
          \nNow it\'s time to initialize databases!\
          \nThe bot uses PostgreSQL and MongoDB so you need to set them running on your host.')