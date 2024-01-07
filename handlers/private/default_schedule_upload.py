# <---------- Python modules ---------->
from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


# <---------- Local modules ---------->
from messages import ms_regular, ms_private
from utilities import ut_logger, ut_handlers, ut_filters
from data_base import operations
from exceptions.ex_handlers import NotEnoughDays, InvalidWeekDay, SundayException, NoLesson, InvalidLessonNumber, NotSuitableLessonNumber
from keyboards import kb_private


# <---------- Variables ---------->
filename = 'default_schedule_upload.py'


# <---------- FSM machine ---------->
class UpdateMainScheduleDailyFSM(StatesGroup):
	sc_days = State()
	sc_weekday_input = State()
	sc_check = State()
	sc_approve = State()


# <---------- Default schedule upload ---------->
async def FSM_message_startUpload(message: types.Message, state: FSMContext):
	"""
	Triggered by '/update' - TEST
	:param message:
	:param state:
	:return:
	"""
	try:
		await message.answer(
			text=ms_private.scheduleSet,
			reply_markup=kb_private.reply_cancel
		)
		await message.answer(
			text=ms_private.studyDays,
			reply_markup=kb_private.inline_mainScheduleDays
		)
		await state.set_state(state=UpdateMainScheduleDailyFSM.sc_days)
		exception = ''
		content = 'Start default schedule upload.'	
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_startUpload',
		exception=exception,
		content=content
	)


async def FSM_callback_query_dayChoice(callback_query: types.CallbackQuery, state: FSMContext):
	try:
		await callback_query.answer()
		data = await state.get_data()
		data['days'] = int(callback_query.data.replace('MainSchedule_Days', ''))
		data['current_day'] = 0
		data['schedule_input'] = 'Основное расписание\n'
		if data['days'] == 5:
			text = ms_private.studyDays_from0to5
		else:
			text = ms_private.studyDays_from0to4
		await callback_query.message.edit_text(
			text=text,
			reply_markup=None
		)
		await state.set_data(data=data)
		await state.set_state(state=UpdateMainScheduleDailyFSM.sc_weekday_input)
		text = await ms_private.currentDaySchedule_accusativeCase(current_day=ms_regular.weekdays_accusativeCase[data["current_day"]].capitalize())
		await callback_query.message.answer(
			text=text,
			reply_markup=kb_private.reply_cancel
		)
		exception = ''
		content = f'Chosen schedule for {data["days"] + 1} days.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='FSM_callback_query_dayChoice',
		exception=exception,
		content=content
	)


async def FSM_message_weekDayInput(message: types.Message, state: FSMContext):
	try:
		await ut_handlers.scheduleMessageToDict(message.text, 1)
		data = await state.get_data()
		data['schedule_input'] += (
			f'{ms_regular.weekdays[data["current_day"]].capitalize()}\n'
			f'{message.text}\n'
		)
		data['current_day'] += 1
		if data['current_day'] == data['days']:
			await state.set_state(UpdateMainScheduleDailyFSM.sc_check)
		await message.answer(text=await ms_private.currentDaySchedule_accusativeCase(current_day=ms_regular.weekdays_accusativeCase[data["current_day"]].capitalize()))
		await state.set_data(data)
		exception = ''
		content = f'Set schedule for {ms_regular.weekdays_accusativeCase[data["current_day"]].capitalize()}.'
	except NoLesson as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		exception = f'No lesson at line {exc.num}.'
		content = ''
	except InvalidLessonNumber as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		exception =f'Invalid lesson number at line {exc.num}.'
		content = ''
	except NotSuitableLessonNumber as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		exception = f'Not suitable lesson number at line {exc.num}.'
		content=''
	except Exception as exc:
		exception = exc
		content = '' 
		await state.clear()

	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_weekDayInput',
		exception=exception,
		content=content
	)


async def FSM_message_checkUpload(message: types.Message, state: FSMContext):
	try:
		await ut_handlers.scheduleMessageToDict(message.text, 1)
		data = await state.get_data()
		data['schedule_input'] += (
			f'{ms_regular.weekdays[data["current_day"]].capitalize()}\n'
			f'{message.text}\n'
		)
		await state.set_data(data)
		await FSM_message_approveUpload(message, state)
		exception = ''
		content = 'Schedule upload checked, appoval TOGO.'
	except NoLesson as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		exception = f'No lesson at line {exc.num}.',
		content=''
	except InvalidLessonNumber as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		exception = f'Invalid lesson number at line {exc.num}.',
		content=''	
	except NotSuitableLessonNumber as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		exception = f'Not suitable lesson number at line {exc.num}.',
		content=''
	except Exception as exc:
		exception = exc,
		content=''
		await state.clear()
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_checkUpload',
		exception=exception,
		content=content
	)


async def FSM_message_approveUpload(message: types.Message, state: FSMContext):
	"""
	Simple one message schedule uploading.
	:param message:
	:param state:
	:return:
	"""
	try:
		data = await state.get_data()
		if await state.get_state() is None:
			schedule_input = message.text
		else:
			schedule_input = data['schedule_input']
		schedule_dict = await ut_handlers.scheduleMessageToDict(schedule_input, 0)
		schedule_text = await ut_handlers.scheduleDictToMessage(schedule_dict, 0)
		subjects = await ut_handlers.scheduleEnumSubjects(schedule_dict, 0)
		text = await ms_private.scheduleApprove(len_subjects=len(subjects))
		for num, subject in enumerate(subjects):
			text += '  ' + subject
			if subject != subjects[-1]:
				text += ','
			if num % 2 != 0:
				text += '\n'
		text += await ms_private.scheduleAppearance(schedule=schedule_text)
		await state.set_state(UpdateMainScheduleDailyFSM.sc_approve)
		data['schedule_dict'] = schedule_dict
		await message.answer(
			text = text,
			reply_markup = kb_private.reply_cancel
		)
		if await operations.getMainSchedule(id=message.from_user.id):
			text = ms_private.scheduleUpdate
		else:
			text = ms_private.scheduleLoad
		await message.answer(
			text=text,
			reply_markup=kb_private.inline_mainScheduleApprove
		)
		await state.set_data(data)
		exception = '',
		content = 'Schedule approved.'
	except NotEnoughDays as exc:
		await message.answer(text=exc.text)
		await state.clear()
		exception = 'Not enough days.',
		content = ''
	except InvalidWeekDay as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		await state.clear()
		exception = f'Invalid week day at line {exc.num}.',
		content = ''
	except SundayException as exc:
		await message.answer(text=exc.text)
		await state.clear()
		exception = 'Sunday in schedule.',
		content = ''
	except NoLesson as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		await state.clear()
		exception = f'No lesson at line {exc.num}.',
		content = ''
	except InvalidLessonNumber as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		await state.clear()
		exception = f'Invalid lesson number at line {exc.num}.',
		content = ''
	except NotSuitableLessonNumber as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		await state.clear()
		exception = f'Not suitable lesson number at line {exc.num}.',
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
		await state.clear()
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_approveUpload',
		exception=exception,
		content=content
	)


async def FSM_callback_query_submitUpload(callback_query: types.CallbackQuery, state: FSMContext):
	try:
		await callback_query.answer()
		await callback_query.message.edit_reply_markup(reply_markup=None)
		data = await state.get_data()
		await operations.setMainSchedule(
			id=callback_query.from_user.id,
			data=data["schedule_dict"]
		)
		await callback_query.message.answer(
			text=ms_private.scheduleLoaded,
			reply_markup=kb_private.reply_commandStartOrHelp
		)
		await state.clear()
		exception = '',
		content = 'Upload submitted.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='FSM_callback_query_submitUpload',
		exception=exception,
		content=content
	)


async def FSM_callback_query_declineUpload(callback_query: types.CallbackQuery, state: FSMContext):
	try:
		await callback_query.answer()
		await callback_query.message.edit_reply_markup(reply_markup=None)
		await callback_query.message.answer(
			text=ms_private.scheduleLoadDecline,
			reply_markup=kb_private.reply_commandStartOrHelp
		)
		await state.clear()
		exception = ''
		content = 'Upload declined.'	
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='FSM_callback_query_declineUpload',
		exception=exception,
		content=content
	)


async def FSM_message_stopUpload(message: types.Message, state: FSMContext):
	try:
		await message.delete()
		await state.clear()
		await message.answer(
			text=ms_private.scheduleLoadDecline,
			reply_markup=kb_private.reply_commandStartOrHelp
		)
		exception = ''
		content = 'Schedule uploading stopped.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_stopUpload',
		exception=exception,
		content=content
	)


async def FSM_message_elseUpload(message: types.Message):
	try:
		await message.delete()
		await message.answer(text=ms_private.scheduleElseUpload)
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_elseUpload',
		exception=exception,
		content=content
	)


async def callback_query_deleteButtons(callback_query: types.CallbackQuery):
	try:
		await callback_query.message.edit_text(
			text=ms_private.scheduleUpdateFinish,
			reply_markup=None
		)
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.message.from_user.id,
		filename=filename,
		function='message_deleteButtons',
		exception=exception,
		content=content
	)


# <---------- Handlers registration ---------->
def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(chat_types=['private']), UserIsGroupAdmin(flag=True)
	:param router:
	:return:
	"""
	router.callback_query.register(FSM_callback_query_submitUpload, F.data == 'MainSchedule_Submit', StateFilter(UpdateMainScheduleDailyFSM.sc_approve))
	router.callback_query.register(FSM_callback_query_declineUpload, F.data == 'MainSchedule_Decline', StateFilter(UpdateMainScheduleDailyFSM.sc_approve))
	router.callback_query.register(callback_query_deleteButtons, F.data.in_({'MainSchedule_Submit', 'MainSchedule_Decline'}))
	router.callback_query.register(FSM_callback_query_dayChoice, F.data.in_({'MainSchedule_Days4', 'MainSchedule_Days5'}), StateFilter(UpdateMainScheduleDailyFSM.sc_days))
	router.message.register(FSM_message_approveUpload, F.text.startswith('Основное расписание'))
	router.message.register(FSM_message_checkUpload, StateFilter(UpdateMainScheduleDailyFSM.sc_check))
	router.message.register(FSM_message_startUpload, Command('update'))
	router.message.register(FSM_message_stopUpload, ut_filters.TextEquals(list_ms=ms_regular.FSM_cancel, data_type='message'), StateFilter(UpdateMainScheduleDailyFSM))
	router.message.register(FSM_message_weekDayInput, StateFilter(UpdateMainScheduleDailyFSM.sc_weekday_input))
	router.message.register(FSM_message_elseUpload, StateFilter(UpdateMainScheduleDailyFSM))
