# <---------- Python modules ---------->
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import json

# <---------- Local modules ---------->
from create_bot import bot
from utilities import ut_logger, ut_handlers, ut_filters
from data_base import operations
# from messages.ms_private import 
from exceptions.ex_handlers import *

# <---------- Variables ---------->
filename = 'homework_show.py'


# <---------- Homework Showing ---------->
async def message_homeworkShow(message: types.Message):
	hw = await operations.getHomework(message.from_user.id)
	print(json.dumps(hw, indent=3, ensure_ascii=False))


# <---------- Handlers registration ---------->
def register_handlers(router: Router):
	router.message.register(message_homeworkShow, ut_filters.TextEquals(list_ms=ms_regular.homeworkShow, data_type='message'))