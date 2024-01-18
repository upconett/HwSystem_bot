# <---------- Python modules ---------->
from aiogram import Router, types, F
from datetime import datetime, timedelta
from dateutil.parser import parse


# <---------- Local modules ---------->
from utilities import ut_logger, ut_handlers, ut_filters
from utilities.ut_handlers import quote_format
from keyboards.kb_private import inline_scheduleNavigate
from messages import ms_regular
from data_base import operations
from exceptions.ex_handlers import *


# <---------- Variables ---------->
filename = 'schedule_show.py'


# <---------- Homework Showing ---------->
async def message_scheduleShowTomorrow(message: types.Message):
	"""
	Show schedule for tomorrow (from now + 12h).
	:param message:
	:return:
	"""
	try:
		date = datetime.now() + timedelta(hours=12)
		weekday = ms_regular.weekdays[date.weekday()]
		text = (
			'<b>📋 Расписание</b>\n'
			f'<b>{weekday.capitalize()} ({date.day} {ms_regular.months_genitive[date.month-1]} {date.year})</b>\n'
		)
		schedule = await operations.getSchedule(message.from_user.id)
		if not schedule:
			schedule = await operations.getMainSchedule(message.from_user.id)
			schedule = schedule[weekday]
		text += await ut_handlers.scheduleDictToMessage(
			schedule=schedule,
			mode=1
		)
		await message.answer(
			text=text,
			reply_markup=inline_scheduleNavigate(date)
		)
		await message.delete()
		exception = ''
		content = 'Showed schedule for tomorrow.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_scheduleShowTomorrow',
		exception=exception,
		content=content
	)
	

async def message_scheduleShowDate(message: types.Message):
	"""
	Show schedule for provided date.\n
	Used via keywords presented in ms_regular.scheduleShow.
	:param message:
	:return:
	"""
	try:
		date = await ut_handlers.ExtractDataShow(
			id=message.from_user.id,
			text=message.text,
			mode=1
		)	
		weekday = ms_regular.weekdays[date.weekday()]
		text = (
			'<b>📋 Расписание</b>\n'
			f'<b>{weekday.capitalize()} ({date.day} {ms_regular.months_genitive[date.month-1]} {date.year})</b>\n'
		)
		schedule = await operations.getSchedule(message.from_user.id)
		if not schedule:
			schedule = await operations.getMainSchedule(message.from_user.id)
			schedule = schedule[weekday]
		text += await ut_handlers.scheduleDictToMessage(
			schedule=schedule,
			mode=1
		)
		await message.answer(
			text=text,
			reply_markup=inline_scheduleNavigate(date)
			)
		await message.delete()
		exception = ''
		content = f'Showed schedule for {date.date()}'
	except InvalidDate as exc:
		await message.answer(
			text=exc.text,
			reply_parameters=quote_format(
				message=message,
				quote=exc.quote
			)
		)
		exception = ''
		content = 'Provided invalid date.'
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_scheduleShowDate',
		exception=exception,
		content=content
	)


async def callback_query_scheduleShowDate(query: types.CallbackQuery):
	"""
	Show schedule for provided date.\n
	Used via inline buttons.
	:param query:
	:return:
	"""
	try:
		date = parse(query.data.replace('Schedule', ''))
		weekday = ms_regular.weekdays[date.weekday()]
		text = (
			'<b>📋 Расписание</b>\n'
			f'<b>{weekday.capitalize()} ({date.day} {ms_regular.months_genitive[date.month-1]} {date.year})</b>\n'
		)
		schedule = await operations.getSchedule(query.from_user.id)
		if not schedule:
			schedule = await operations.getMainSchedule(query.from_user.id)
			schedule = schedule[weekday]
		text += await ut_handlers.scheduleDictToMessage(
			schedule=schedule,
			mode=1
		)
		await query.message.edit_text(
			text=text,
			reply_markup=inline_scheduleNavigate(date)
		)
		exception = ''
		content = f'Showed schedule on {date.date()}'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=query.from_user.id,
		filename=filename,
		function='callback_query_scheduleShowDate',
		exception=exception,
		content=content
	)


# <---------- Handlers registration ---------->
def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(chat_types=['private'], data_type='message'), UserPresenceInGroup()
	:param router:
	:return:
	"""
	router.message.register(message_scheduleShowTomorrow, ut_filters.TextEquals(list_ms=ms_regular.scheduleShow, data_type='message'))
	router.message.register(message_scheduleShowDate, F.text.lower().startswith(tuple(ms_regular.scheduleShow)))

	router.callback_query.register(callback_query_scheduleShowDate, F.data.startswith('Schedule'))
	