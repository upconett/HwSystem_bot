# <---------- Python modules ---------->
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import json

# <---------- Local modules ---------->
from create_bot import bot
from utilities import ut_logger, ut_handlers
from data_base import operations
# from messages.ms_private import 
from exceptions.ex_handlers import *

# <---------- Variables ---------->
filename = 'homework_show.py'


# <---------- Handlers homework ---------->
async def message_homeworkShow