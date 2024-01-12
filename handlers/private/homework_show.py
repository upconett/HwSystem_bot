# <---------- Python modules ---------->
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
import json

# <---------- Local modules ---------->
from create_bot import bot
from utilities import ut_logger, ut_handlers, ut_filters
from messages import ms_private
from data_base import operations
# from messages.ms_private import 
from exceptions.ex_handlers import *

# <---------- Variables ---------->
filename = 'homework_show.py'


# <---------- Homework Showing ---------->
async def message_homeworkShowTomorrow(message: types.Message):
	try:
		date = datetime.now() + timedelta(hours=12)
		tasks = await operations.getHomework(
			id=message.from_user.id,
			date=date
		)
		media_group = []
		has_media = False
		if tasks:
			schedule = await operations.getMainSchedule(message.from_user.id)
			if not schedule:
				await message.answer(ms_private.noMainSchedule)
				return
			for lesson in tasks:
				if tasks[lesson]['photos']:
					has_media = True
					for id in tasks[lesson]['photos']:
						media_group.append(types.InputMediaPhoto(media=id))
		text = ms_private.homeworkShow(
			date=date,
			tasks=tasks,
			schedule=schedule[ms_regular.weekdays[date.weekday()].capitalize()]
		)
		if has_media:
			media_group[0] = types.InputMediaPhoto(
				media=media_group[0].media,
				caption=text
			)
			await message.answer_media_group(media=media_group)
		else:
			await message.answer(text=text)
	except ValueError as exc:
		print(exc)
	

async def message_homeworkShowDate(message: types.Message):
	try:
		date = await ut_handlers.homeworkExtractDataShow(
			id=message.from_user.id,
			text=message.text
		)
		print(date)
	except ValueError as exc:
		print(exc)


# <---------- Handlers registration ---------->
def register_handlers(router: Router):
	router.message.register(message_homeworkShowTomorrow, ut_filters.TextEquals(list_ms=ms_regular.homeworkShow, data_type='message'))
	router.message.register(message_homeworkShowDate, F.text.lower().startswith(tuple(ms_regular.homeworkShow)))