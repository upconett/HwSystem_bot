# <---------- Python modules ---------->
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


# <---------- Local modules ---------->
from create_bot import psql
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'group_enter.py'


# <---------- FSM machine ---------->
class FSMGroupEnter(StatesGroup):
	name = State()
	password = State()


# <---------- Main functions ---------->
async def callback_query_enterGroupStart(callback_query: types.CallbackQuery, state: FSMContext):
	"""
	Starts group entry FSM machine from callback button.
	:param state:
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		await callback_query.message.delete()
		await callback_query.message.delete(
			text=ms_private.groupEnterName,
			reply_markup=kb_private.reply_cancel
		)
		await state.set_state(FSMGroupEnter.name)
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_enterGroupStart',
		exception=exception,
		content=content
	)


async def message_enterGroupStart(message: types.Message, state: FSMContext):
	"""
	Starts group entry FSM machine.
	:param message:
	:param state:
	:return:
	"""
	try:
		await message.delete()
		await message.answer(
			text=ms_private.groupEnterName,
			reply_markup=kb_private.reply_cancel
		)
		await state.set_state(FSMGroupEnter.name)
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_enterGroupStart',
		exception=exception,
		content=content
	)


async def FSM_message_cancel(message: types.Message, state: FSMContext):
	"""
	Cancel active FSM machine.
	:param message:
	:param state:
	:return:
	"""
	try:
		current_state = await state.get_state()
		if not current_state:
			text = 'Нечего отменять 🤷'
			content = 'No active state.'
		else:
			await state.clear()
			text = 'Отменено 👍'
			content = 'State aborted.'
		await message.answer(
			text=text,
			reply_markup=kb_private.reply_commandStartOrHelp
		)
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_cancel',
		exception=exception,
		content=content
	)


async def FSM_message_enterGroupName(message: types.Message, state: FSMContext):
	"""
	Set name for group.
	:param message:
	:param state:
	:return:
	"""
	try:
		response = await psql.select(
			table='groups',
			what='*',
			where='group_name',
			where_value=message.text
		)
		if response:
			await state.update_data(name=message.text)
			text = ms_private.groupEnterPassword
			await state.set_state(state=FSMGroupEnter.password)
			content = f'Chosen group "{message.text}".'
		else:
			text = ms_private.groupEnterName_noGroup
			content = f'No group with name "{message.text}".'
		await message.answer(
			text=text,
			reply_markup=kb_private.reply_cancel
		)
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_enterGroupName',
		exception=exception,
		content=content
	)


async def FSM_message_enterGroupPassword(message: types.Message, state: FSMContext):
	"""
	Set password for group.
	:param message:
	:param state:
	:return:
	"""
	try:
		data = await state.get_data()
		response = (await psql.select(
			table='groups',
			what='*',
			where='group_name',
			where_value=data['name']
		))
		if response[0][2] == message.text:
			await state.update_data(password=message.text)
			await psql.update(
				table='users',
				what='group_id',
				what_value=response[0][0],
				where='id',
				where_value=message.from_user.id
			)
			text = await ms_private.groupEnterFinish(group_name=response[0][1])
			await message.answer(
				text=ms_private.groupEnterPassword_correct,
				reply_markup=kb_private.reply_commandStartOrHelp
			)
			await message.answer(
				text=text,
				reply_markup=kb_private.inline_groupPanelForMember
			)
			await state.clear()
			content = 'Entered group.'
		else:
			await message.answer(
				text=ms_private.groupEnterPassword_incorrect,
				reply_markup=kb_private.reply_cancel
			)
			content = f'Incorrect password for group "{response[0][1]}".'
		await message.delete()
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_enterGroupPassword',
		exception=exception,
		content=content
	)


# <---------- Registration handlers ---------->
def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(chat_types=['private'], data_type='message'), ~UserPresenceInGroup()
	:param router:
	:return:
	"""
	router.message.register(message_enterGroupStart, ut_filters.TextEquals(list_ms=ms_regular.groupEntry, data_type='message'))
	router.callback_query.register(callback_query_enterGroupStart, F.data == 'EnterGroup')
	router.message.register(FSM_message_cancel, ut_filters.TextEquals(list_ms=ms_regular.FSM_cancel, data_type='message'), StateFilter('*'))
	router.message.register(FSM_message_enterGroupName, FSMGroupEnter.name)
	router.message.register(FSM_message_enterGroupPassword, FSMGroupEnter.password)
