# <---------- Импорт функций Aiogram ---------->
from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


# <---------- Импорт локальных функций ---------->
from create_bot import bot
from data_base.operation import db_psql_UserData, db_psql_GetMainSchedule, db_psql_UpdateMainSchedule
from exceptions.ex_handlers import NotEnoughDays, InvalidWeekDay,\
    SundayException, NoLesson, InvalidLessonNumber, NotSuitableLessonNumber
from keyboards.kb_client import *
from keyboards.kb_schedule import *
from utilities.ut_handlers import ut_filterForMDV2, ut_ScheduleMessageToDict,\
	 ut_ScheduleDictToMessage, ut_ScheduleEnumSubjects
from utilities.ut_logger import ut_LogCreate


# <---------- Переменные ---------->
filename = 'schedule.py'
days_0 = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
days_1 = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу']


# <---------- Машина состояний ---------->
class UpdateMainScheduleDailyFSM(StatesGroup):
	sc_days = State()
	sc_weekday_input = State()	
	sc_check = State()
	sc_approve = State()


# <---------- Роутер  ---------->
router = Router()
router.message()


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
async def schedule_FSM_ApproveUpload(message: types.Message, state: FSMContext):
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
			exception = 'Used from group.'
			await state.clear()
		else:
			user_data = await db_psql_UserData(message.from_user.id)
			if user_data['group_id']:
				if user_data['group_admin']:
					if await state.get_state() is None:
						schedule_input = message.text
					else:
						data = await state.get_data()
						schedule_input = data['schedule_input']
					schedule_dict = await ut_ScheduleMessageToDict(schedule_input, 0)
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
					await state.set_state(UpdateMainScheduleDailyFSM.sc_approve)
					async with state.proxy() as data:
						data['schedule_dict'] = schedule_dict
			await message.answer(
				text, 
				reply_markup=kb_reply_MainSchedule_Cancel
			)
			if await db_psql_GetMainSchedule(message.from_user.id):
				text = '<b>Обновить основное расписание?</b>'
			else: 
				text = '<b>Установить основное раписание?</b>'
			await message.answer(
				text,
				reply_markup=kb_inline_MainSchedule_Approve
			)

	except NotEnoughDays:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			'В расписании должно быть не менее <b>5 дней</b>!\n'
			)
		await state.clear()
	except InvalidWeekDay as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* неправильно записан день недели\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.clear()
	except SundayException as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			'Вы что учитесь по воскресеньям? 😶‍🌫️\n'
			'Если и правда так, <a href="https://t.me/SteePT">напишите нам</a>, мы всё исправим!\n'
		)
		await state.clear()
	except NoLesson as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* не указано название предмета\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.clear()
	except InvalidLessonNumber as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'В строке *№{exception.num}* неправильно указан номер урока\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.clear()
	except NotSuitableLessonNumber as exception:
		await message.answer(
			'Основное расписание не сохранено ❌\n'
			f'Ошибка в строке *№{exception.num}*\n'
			'Номер урока не может быть меньше *0* или больше *10*\!\n'
			f'> {await ut_filterForMDV2(exception.line)}',
			parse_mode='MarkdownV2'
		)
		await state.clear()
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='schedule_FSM_ApproveUpload',
			exception=exception,
			content=''
		)
		await state.clear()


async def schedule_FSM_StartUpload(message: types.Message, state: FSMContext):
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
			if await client_IsGroupMember(message.from_user.id):
				await message.answer(
					'*Изменение основного расписания ✏️*\n',
					parse_mode='Markdown',
					reply_markup=kb_reply_MainSchedule_Cancel
					)
				await message.answer(
					'В какие дни вы учитесь? ✍️',
					reply_markup=kb_inline_MainSchedule_Days
					)
				await state.set_state(UpdateMainScheduleDailyFSM.sc_days)
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
		data['current_day'] = 0
		data['schedule_input'] = 'Основное расписание\n'
	if data['days'] == 5:
		text = 'С понедельника по субботу'
	else:
		text = 'С понедельника по пятницу'
	await query.message.edit_text(
		text=text, 
		reply_markup=None
		)
	await UpdateMainScheduleDailyFSM.next()
	await query.message.answer(
		f'Введите расписание на {days_1[data["current_day"]]} 👇',
		reply_markup=kb_reply_MainSchedule_Cancel
		)
	await query.answer()


async def schedule_FSM_WeekDayInput(message: types.Message, state: FSMContext):
	try:
		await ut_ScheduleMessageToDict(message.text, 1)
		async with state.proxy() as data:
			data['schedule_input'] += (
				f'{days_0[data["current_day"]]}\n'
				f'{message.text}\n'
				)
			data['current_day'] += 1 
			if data['current_day'] == data['days']:
				await UpdateMainScheduleDailyFSM.next()
			await message.answer(
				f'Введите расписание на {days_1[data["current_day"]]} 👇'
				)
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
		await state.clear()

	
async def schedule_FSM_CheckUpload(message: types.Message, state: FSMContext):
	try:
		await ut_ScheduleMessageToDict(message.text, 1)
		async with state.proxy() as data:
			data['schedule_input'] += (
				f'{days_0[data["current_day"]]}\n'
				f'{message.text}\n'
				)
		await schedule_FSM_ApproveUpload(message, state)
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
		await state.clear()


async def schedule_FSM_SubmitUpload(query: types.CallbackQuery, state: FSMContext):
	try:
		await query.message.edit_reply_markup(reply_markup=None)
		async with state.proxy() as data:
			if await db_psql_UpdateMainSchedule(query.from_user.id, data["schedule_dict"]):
				await query.message.answer(
					'Основное расписание установлено!',
					reply_markup=kb_reply_CommandStartOrHelp
				)
			else:
				await query.message.answer(
					'Ошибка в установке расписания...',
					reply_markup=kb_reply_CommandStartOrHelp
				)
		await state.clear()
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
		await query.message.edit_reply_markup(reply_markup=None)
		await query.message.answer(
			'Обновление основного расписания отменено ⭕', 
			reply_markup=kb_reply_CommandStartOrHelp
		)
		await state.clear()
		await query.answer()
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='schedule_FSM_DeclineUpload',
			exception=exception,
			content=''
		)


async def schedule_FSM_StopUpload(message: types.Message, state: FSMContext):
	await message.delete()
	await state.clear()
	await message.answer(
		'Обновление основного расписания отменено ⭕', 
		reply_markup=kb_reply_CommandStartOrHelp
		)


async def schedule_FSM_ElseUpload(message: types.Message):
	await message.delete()
	await message.answer(
		'Вы не можете использовать другие функции!\n'
		'Сначала <b>завершите обновление расписания!</b>'
		)


async def schedule_deleteButtons(query: types.CallbackQuery):
	await query.message.edit_text(
		text='Обновления расписания завершено...',
		reply_markup=None
	)


def register_handlers():
	router.callback_query.register(schedule_FSM_SubmitUpload, F.data == 'MainSchedule_Submit', StateFilter(UpdateMainScheduleDailyFSM.sc_approve))
	router.callback_query.register(schedule_FSM_DeclineUpload, F.data == 'MainSchedule_Decline', StateFilter(UpdateMainScheduleDailyFSM.sc_approve))
	router.callback_query.register(schedule_deleteButtons, F.text.in_({'MainSchedule_Submit','MainSchedule_Decline'}))
	router.callback_query.register(schedule_FSM_DayChoise, F.data.in_({'MainSchedule_Days4', 'MainSchedule_Days5'}), StateFilter(UpdateMainScheduleDailyFSM.sc_days))
	router.message.register(schedule_FSM_ApproveUpload, F.text.startswith('Основное расписание'))
	router.message.register(schedule_FSM_CheckUpload, StateFilter(UpdateMainScheduleDailyFSM.sc_check))
	router.message.register(schedule_FSM_StartUpload, Command('update'))
	router.message.register(schedule_FSM_WeekDayInput, StateFilter(UpdateMainScheduleDailyFSM.sc_weekday_input))
	router.message.register(schedule_FSM_StopUpload, F.text == 'Отмена ❌', StateFilter(UpdateMainScheduleDailyFSM))
	router.message.register(schedule_FSM_ElseUpload, StateFilter(UpdateMainScheduleDailyFSM))
