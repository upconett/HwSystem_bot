# <---------- Python modules ---------->
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


# <---------- Local modules ---------->
from create_bot import bot, psql
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters, ut_handlers
from data_base import operations


# <---------- Variables ---------->
filename = 'group_create.py'


# <---------- FSM machine ---------->
class FSMGroupRegister(StatesGroup):
	name = State()
	password = State()


# <---------- Main functions ---------->
async def callback_query_registerGroupStart(callback_query: types.CallbackQuery, state: FSMContext):
	"""
	Starts group registration FSM machine from callback button.
	:param state:
	:param callback_query:
	:return:
	"""
	try:
		await bot.delete_message(
			chat_id=callback_query.from_user.id,
			message_id=callback_query.message.message_id
		)
		await bot.send_message(
			chat_id=callback_query.from_user.id,
			text=ms_private.groupRegisterName,
			reply_markup=kb_private.reply_cancel
		)
		await state.set_state(FSMGroupRegister.name)
		exception = ''
		content = 'Started group registration.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_registerGroupStart',
		exception=exception,
		content=content
	)


async def message_registerGroupStart(message: types.Message, state: FSMContext):
	"""
	Starts group registration FSM machine.
	:param message:
	:param state:
	:return:
	"""
	try:
		await message.delete()
		await message.answer(
			text=ms_private.groupRegisterName,
			reply_markup=kb_private.reply_cancel
		)
		await state.set_state(state=FSMGroupRegister.name)
		exception = ''
		content = 'Started group registration.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_registerGroupStart',
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
			exception = 'No active state.'
			content = ''
		else:
			await state.clear()
			text = 'Отменено 👍'
			exception = ''
			content = 'Register'
		await message.answer(
			text=text,
			reply_markup=kb_private.reply_commandStartOrHelp
		)
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


async def FSM_message_registerGroupName(message: types.Message, state: FSMContext):
	"""
	Set name for group.
	:param message:
	:param state:
	:return:
	"""
	try:
		await state.update_data(name=message.text)
		await message.answer(
			text=ms_private.groupRegisterPassword,
			reply_markup=kb_private.reply_cancel
		)
		await state.set_state(state=FSMGroupRegister.password)
		exception = ''
		content = f'Set group name "{message.text}".'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_registerGroupName',
		exception=exception,
		content=content
	)


async def FSM_message_registerGroupPassword(message: types.Message, state: FSMContext):
	"""
	Set password for group.
	:param message:
	:param state:
	:return:
	"""
	try:
		await state.update_data(password=message.text)
		data = await state.get_data()
		await operations.insertGroup(
			group_name=data['name'],
			group_password=data['password'],
			owner_id=message.from_user.id,
		)
		group_id = (await psql.select(
			table='groups',
			what='group_id',
			where='group_name',
			where_value=data['name']
		))[0]
		await psql.update(
			table='users',
			what='group_id',
			what_value=group_id,
			where='id',
			where_value=message.from_user.id
		)
		group_name = await ut_handlers.ut_filterForMDV2(data['name'])
		group_password = await ut_handlers.ut_filterForMDV2(data['password'])
		text = await ms_private.groupRegisterFinish(
			group_name=group_name,
			group_password=group_password
		)
		await message.answer(
			text=text,
			reply_markup=kb_private.reply_commandStartOrHelp,
			parse_mode='MarkdownV2'
		)
		await message.delete()
		await state.clear()
		exception = ''
		content = 'Registered group.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_registerGroupName',
		exception=exception,
		content=content
	)


# <---------- Registration handlers ---------->
def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(chat_types=['private'])
	:param router:
	:return:
	"""
	router.callback_query.register(callback_query_registerGroupStart, F.data == 'CreateGroup')
	router.message.register(message_registerGroupStart, ut_filters.TextEquals(list_ms=ms_regular.groupRegistration, data_type='message'))
	router.message.register(FSM_message_cancel, ut_filters.TextEquals(list_ms=ms_regular.FSM_cancel, data_type='message'), StateFilter(None))
	router.message.register(FSM_message_registerGroupName, FSMGroupRegister.name)
	router.message.register(FSM_message_registerGroupPassword, FSMGroupRegister.password)
