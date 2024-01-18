# <---------- Python modules ---------->
from aiogram import Router, types, F
from datetime import datetime, timedelta
from dateutil.parser import parse


# <---------- Local modules ---------->
from utilities import ut_logger, ut_handlers, ut_filters
from utilities.ut_handlers import quote_format
from keyboards.kb_private import inline_homeworkNavigate
from messages import ms_private, ms_regular
from data_base import operations
from exceptions.ex_handlers import *


# <---------- Variables ---------->
filename = 'homework_show.py'


# <---------- Homework Showing ---------->
async def message_homeworkShowTomorrow(message: types.Message):
	"""
	Show homework for tomorrow (from now + 12h).
	:param message:
	:return:
	"""
	try:
		date = datetime.now() + timedelta(hours=12)
		tasks = await operations.getHomework(
			id=message.from_user.id,
			date=date
		)
		next_date, prev_date = await operations.closestDates(message.from_user.id, date)
		media_group = []
		has_media = False
		schedule = await operations.getMainSchedule(message.from_user.id)
		if tasks:
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
			schedule=schedule[ms_regular.weekdays[date.weekday()]]
		)
		if has_media:
			media_group[0] = types.InputMediaPhoto(
				media=media_group[0].media,
				caption=text
			)
			await message.answer_media_group(media=media_group)
		else:
			await message.answer(text=text)
		if next_date or prev_date:
			await message.answer(
				text='Другой день 🔗',
				reply_markup=inline_homeworkNavigate(
					date,
					next_date, 
					prev_date
				)
			)
		await message.delete()
		exception = ''
		content = 'Showed homework for tomorrow.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_homeworkShowTomorrow',
		exception=exception,
		content=content
	)
	

async def message_homeworkShowDate(message: types.Message):
	"""
	Show homework for provided date.\n
	Used via keywords presented in ms_regular.homeworkShow.
	:param message:
	:return:
	"""
	try:
		date = await ut_handlers.ExtractDataShow(
			id=message.from_user.id,
			text=message.text,
			mode=0
		)
		tasks = await operations.getHomework(
			id=message.from_user.id,
			date=date
		)
		next_date, prev_date = await operations.closestDates(message.from_user.id, date)
		media_group = []
		has_media = False
		schedule = await operations.getMainSchedule(message.from_user.id)
		if tasks:
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
			schedule=schedule[ms_regular.weekdays[date.weekday()]]
		)
		if has_media:
			media_group[0] = types.InputMediaPhoto(
				media=media_group[0].media,
				caption=text
			)
			await message.answer_media_group(media=media_group)
		else:
			await message.answer(text=text)
		if next_date or prev_date:
			await message.answer(
				text='Другой день 🔗',
				reply_markup=inline_homeworkNavigate(
					date,
					next_date, 
					prev_date
				)
			)
		await message.delete()
		exception = ''
		content = f'Showed homework for {date.date()}'
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
		function='message_homeworkShowDate',
		exception=exception,
		content=content
	)


async def callback_query_homeworkShowDate(query: types.CallbackQuery):
	"""
	Show homework for provided date.\n
	Used via inline buttons.
	:param query:
	:return:
	"""
	try:
		date = parse(query.data.replace('Homework', ''))
		tasks = await operations.getHomework(
			id=query.from_user.id,
			date=date
		)
		next_date, prev_date = await operations.closestDates(query.from_user.id, date)
		media_group = []
		has_media = False
		schedule = await operations.getMainSchedule(query.from_user.id)
		if tasks:
			if not schedule:
				await query.answer(ms_private.noMainSchedule)
				return
			for lesson in tasks:
				if tasks[lesson]['photos']:
					has_media = True
					for id in tasks[lesson]['photos']:
						media_group.append(types.InputMediaPhoto(media=id))
		text = ms_private.homeworkShow(
			date=date,
			tasks=tasks,
			schedule=schedule[ms_regular.weekdays[date.weekday()]]
		)
		if has_media:
			media_group[0] = types.InputMediaPhoto(
				media=media_group[0].media,
				caption=text
			)
			await query.message.answer_media_group(media=media_group)
		else:
			await query.message.answer(text=text)
		if next_date or prev_date:
			await query.message.answer(
				text='Другой день 🔗',
				reply_markup=inline_homeworkNavigate(
					date,
					next_date, 
					prev_date
				)
			)
		await query.message.delete()
		exception = ''
		content = f'Showed homework on {date.date()}'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=query.from_user.id,
		filename=filename,
		function='callback_query_homeworkShowDate',
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
	router.message.register(message_homeworkShowTomorrow, ut_filters.TextEquals(list_ms=ms_regular.homeworkShow, data_type='message'))
	router.message.register(message_homeworkShowDate, F.text.lower().startswith(tuple(ms_regular.homeworkShow)))

	router.callback_query.register(callback_query_homeworkShowDate, F.data.startswith('Homework'))
	