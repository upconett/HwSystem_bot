# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from json import dumps


# <---------- Импорт локальных функций ---------->
from create_bot import bot
from data_base.operation import db_psql_UserData
from exceptions.ex_handlers import NotEnoughDays, InvalidWeekDay,\
    SundayException, NoLesson, InvalidLessonNumber, NotSuitableLessonNumber	#InvalidLesson
from keyboards.kb_client import *
from keyboards.kb_schedule import *
from utilities.ut_handlers import ut_filterForMDV2, ut_ScheduleMessageToDict,\
	 ut_ScheduleDictToMessage, ut_ScheduleEnumSubjects
from utilities.ut_logger import ut_LogCreate


# <---------- Константы ---------->
filename = 'schedule.py'
states = ['sc_monday', 'sc_tuesday', 'sc_wednesday', 'sc_thursday', 'sc_friday', 'sc_saturday']
days_0 = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
days_1 = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу']


# <---------- Машина состояний ---------->
class UpdateMainScheduleDailyFSM(StatesGroup):
	sc_days = State()
	sc_tuesday = State()
	sc_wednesday = State()
	sc_thursday = State()
	sc_friday = State()
	sc_saturday = State()
	sc_check = State()
	sc_approve = State()

all_states = [UpdateMainScheduleDailyFSM.sc_days, UpdateMainScheduleDailyFSM.sc_tuesday, 
			  UpdateMainScheduleDailyFSM.sc_wednesday, UpdateMainScheduleDailyFSM.sc_thursday, UpdateMainScheduleDailyFSM.sc_friday, 
			  UpdateMainScheduleDailyFSM.sc_saturday, UpdateMainScheduleDailyFSM.sc_check, UpdateMainScheduleDailyFSM.sc_approve]


# <---------- Вспомогательные функции ---------->
async def client_IsGroupMember(id:int) -> bool:
	"""
	If client is in any group.
	:param id:
	:return:
	"""
	client_data = await db_psql_UserData(id=id)
	if client_data['group_id']:
		return True
	return False


# <---------- Handler функции ---------->
async def schedule_ApproveUpload(message: types.Message, state: FSMContext, mode: int):
	"""
	Simple one message schedule uploading.
	:param message:
	:return:
	"""
	try:
		if message.chat.type in ['supergroup', 'group']:
			await bot.send_message(
				chat_id=message.from_user.id,
				text=f'Устанавливать расписание можно только в личных сообщениях!\n',
				reply_markup=kb_reply_CommandStartOrHelp
				)
			content = 'No database operations.'
			exception = 'Used from group.'
			await state.finish()
		else:
			user_data = await db_psql_UserData(message.from_id)
			# print(user_data)
			if user_data['group_id']:
				if user_data['group_admin']:
					if mode == 0:
						async with state.proxy as data:
							schedule_dict = await ut_ScheduleMessageToDict()
					if len(message.text.split('\n')) > 1:
						schedule_dict = await ut_ScheduleMessageToDict(message.text, 0)
						schedule_txt = await ut_ScheduleDictToMessage(schedule_dict, 0)
						subjects = await ut_ScheduleEnumSubjects(schedule_dict, 0)
						text = (
							'<b>Подтверждение расписания</b> 📋\n'
							f'<b>В расписании {len(subjects)} предметов:</b>\n')
						for num, subject in enumerate(subjects):
							text += '  ' + subject
							if subject != subjects[-1]:
								text += ','
							if num % 2 != 0: text += '\n'
						text += f'\n\n<b>Расписание будет записано так:</b>\n\n{schedule_txt}'
						await UpdateMainScheduleDailyFSM.sc_approve.set()
						async with state.proxy() as data:
							data['schedule_dict'] = schedule_dict
			await message.answer(
				text, 
				reply_markup=kb_reply_MainSchedule_Cancel
				)
			await message.answer(
				'<b>Подтвердить обновление основного расписания?</b>',
				reply_markup=kb_inline_MainSchedule_Approve
			)

	except NotEnoughDays:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			'В расписании должно быть не менее <b>5 дней</b>!\n'
			)
		await state.finish()
	except InvalidWeekDay as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* неправильно записан день недели\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.finish()
	except SundayException as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			'Вы что учитесь по воскресеньям? 😶‍🌫️\n'
			'Если и правда так, <a href="https://t.me/SteePT">напишите нам</a>, мы всё исправим!\n'
		)
		await state.finish()
	# except InvalidLesson as exception:
		# await message.answer(
			# 'Основное расписание не сохранено ❌\n'
			# f'В строке <b>№{exception.num}</b> неправильно записан урок!\n'
			# f'{exception.line}'	
		# )
	except NoLesson as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* не указано название предмета\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.finish()
	except InvalidLessonNumber as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* неправильно указан номер урока\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.finish()
	except NotSuitableLessonNumber as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'Ошибка в строке *№{exception.num}*\n'
			'Номер урока не может быть меньше *0* или больше *10*\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.finish()
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='schedule_FSM_ApproveUpload',
			exception=exception,
			content=''
		)
		await state.finish()


async def schedule_FSM_StartUpload(message: types.Message):
	"""
	Triggered by '/update' - TEST
	:param message:
	:return:
	"""
	try:
		if message.chat.type in ['supergroup', 'group']:
			await bot.send_message(
				chat_id=message.from_user.id,
				text=f'{message.text} можно использовать только в личных сообщениях!\n',
				reply_markup=kb_reply_CommandStartOrHelp
				)
			await message.delete()
			content = 'No database operations.'
			exception = 'Used from group.'
		else:
			if await client_IsGroupMember(message.from_id):
				await message.answer(
					'*Изменение основного расписания ✏️*\n',
					parse_mode='Markdown',
					reply_markup=kb_reply_MainSchedule_Cancel
					)
				await message.answer(
					'В какие дни вы учитесь? ✍️',
					reply_markup=kb_inline_MainSchedule_Days
					)
				await UpdateMainScheduleDailyFSM.sc_days.set()
			else:
				await message.answer('Вы не состоите в группе. ❌\n')
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='schedule_FSM_StartUpload',
			exception=exception,
			content=''
		)


async def schedule_FSM_DayChoise(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['days'] = int(query.data.replace('MainSchedule_Days', ''))
	if data['days'] == 1:
		text = 'С понедельника по субботу'
	else:
		text = 'С понедельника по пятницу'
	await query.message.edit_text(
		text=text, 
		reply_markup=None
		)
	await query.message.answer(
		'Введите расписание на Понедельник 👇',
		reply_markup=kb_reply_MainSchedule_Cancel
		)
	await UpdateMainScheduleDailyFSM.next()
	await query.answer()


async def schedule_FSM_WeekDayInput(message: types.Message, state: FSMContext):
	try:
		if message.text == 'Отмена ❌':
			await schedule_FSM_StopUpload(message, state)
			return
		schedule_dict = await ut_ScheduleMessageToDict(message.text, 1)
		str_state = await state.get_state()
		str_state = str(str_state).replace('UpdateMainScheduleDailyFSM:', '')
		async with state.proxy() as data:
			data[str_state] = schedule_dict
			day = days_1[states.index(str_state)]
			if day == 'Субботу' and data['days'] == 1:
				await message.answer(f"Введите расписание на {day}. 👇")
				await UpdateMainScheduleDailyFSM.next()
			else:
				await schedule_ApproveUpload(message, state, 1)
	except NoLesson as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* не указано название предмета\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
	except InvalidLessonNumber as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* неправильно указан номер урока\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
	except NotSuitableLessonNumber as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'Ошибка в строке *№{exception.num}*\n'
			'Номер урока не может быть меньше *0* или больше *10*\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='schedule_FSM_WeekDayInput',
			exception=exception,
			content=''
		)
		await state.finish()


async def schedule_FSM_SubmitUpload(query: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			await query.message.answer(
				'Подтверждено!\n\n'
				f'{dumps(data["schedule_dict"], indent=2, ensure_ascii=False)}',
				reply_markup=kb_reply_CommandStartOrHelp
				)
		await state.finish()
		await query.answer()
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='schedule_FSM_SubmitUpload',
			exception=exception,
			content=''
		)


async def schedule_FSM_DeclineUpload(query: types.CallbackQuery, state: FSMContext):
	try:
		await query.message.answer(
			'Обновление основного расписания отменено ⭕', 
			reply_markup=kb_reply_CommandStartOrHelp
		)
		await state.finish()
		await query.answer()
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='schedule_FSM_DeclineUpload',
			exception=exception,
			content=''
		)


async def schedule_FSM_ElseUpload(message: types.Message, state: FSMContext):
	await message.delete()
	await message.answer(
		'Вы не можете использовать другие функции!\n'
		'Сначала <b>завершите обновление расписания!</b>'
		)


async def schedule_FSM_StopUpload(message: types.Message, state: FSMContext):
	await message.delete()
	await state.finish()
	await message.answer(
		'Обновление основного расписания отменено ⭕', 
		reply_markup=kb_reply_CommandStartOrHelp
		)


async def schedule_deleteButtons(query: types.CallbackQuery):
	await query.message.edit_text(
		text='Обновления расписания завершено...',
		reply_markup=None
	)


def register_handlers_schedule(dp: Dispatcher):
	"""
	Регистрация всех message и callback хендлеров для сценария: 'Изменение Основного Расписания'.
	:param dp:
	:return:
	"""
	dp.register_callback_query_handler(schedule_FSM_SubmitUpload, Text('MainSchedule_Submit'), state=[UpdateMainScheduleDailyFSM.sc_approve])
	dp.register_callback_query_handler(schedule_FSM_DeclineUpload, Text('MainSchedule_Decline'), state=[UpdateMainScheduleDailyFSM.sc_approve])
	dp.register_callback_query_handler(schedule_deleteButtons, Text(['MainSchedule_Submit','MainSchedule_Decline']))

	dp.register_callback_query_handler(schedule_FSM_DayChoise, Text(['MainSchedule_Days1', 'MainSchedule_Days2']), state=UpdateMainScheduleDailyFSM.sc_days)

	dp.register_message_handler(schedule_FSM_ApproveUpload, Text(startswith='Основное расписание'))
	dp.register_message_handler(schedule_FSM_ApproveUpload, Text(startswith='Основное расписание'), state=[UpdateMainScheduleDailyFSM.sc_approve])
	dp.register_message_handler(schedule_FSM_StartUpload, Text(['/update']))
	dp.register_message_handler(schedule_FSM_WeekDayInput, state=[UpdateMainScheduleDailyFSM.sc_tuesday, 
		UpdateMainScheduleDailyFSM.sc_wednesday, UpdateMainScheduleDailyFSM.sc_thursday,
		UpdateMainScheduleDailyFSM.sc_friday, UpdateMainScheduleDailyFSM.sc_saturday])
	dp.register_message_handler(schedule_FSM_StopUpload, Text('Отмена ❌'), state=all_states)
	dp.register_message_handler(schedule_FSM_ElseUpload, state=all_states)
