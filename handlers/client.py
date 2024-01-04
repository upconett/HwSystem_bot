# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.state import State, StatesGroup


# <---------- Импорт локальных функций ---------->
from create_bot import bot, psql
from data_base.operation import db_psql_UserData, db_psql_InsertUser
from messages.ms_client import *
from messages.ms_regular import *
from keyboards.kb_client import *
from utilities.ut_logger import ut_LogCreate
from utilities.ut_filters import filter_ChatType


# <---------- Переменные ---------->
router = Router()
filename = 'client.py'


# <---------- Машины состояния ---------->
class FSMGroupRegister(StatesGroup):
	name = State()
	password = State()


# <---------- Вспомогательные функции ---------->
async def client_help_ChatIsGroup(message: types.Message):
	if message.chat.type == 'supergroup' or message.chat.type == 'group':
		await bot.send_message(
			chat_id=message.from_user.id,
			text=f'{message.text} можно использовать только в личных сообщениях!',
			reply_markup=kb_reply_CommandStartOrHelp
		)
		await message.delete()
		return True
	else:
		return False


async def client_help_GroupPanel(id: int, chat_id: int, message_id: int = None):
	"""
	Used for callback and message handlers to display the group panel.
	:param id: Telegram ID
	:param chat_id: Telegram chat ID
	:param message_id: Telegram parent message ID
	:return:
	"""
	data = await db_psql_UserData(id=id)
	if not data['group_id']:
		text = mscl_GroupPanel_NoMember
		reply_markup = kb_inline_GroupNoMemberPanel
		content = 'Called the group panel without being a group member.'
	else:
		is_owner = (await psql.select(
			table='groups',
			what='owner_id',
			where='group_id',
			where_value=data['group_id']
		))[0][0]
		if is_owner == id:
			text = mscl_GroupPanel_Owner
			reply_markup = kb_inline_GroupOwnerPanel
			content = 'Called the group panel as the creator of the group.'
		else:
			text = mscl_GroupPanel_Member
			reply_markup = kb_inline_GroupMemberPanel
			content = 'Called the group panel as a group member.'
	if message_id:
		await bot.edit_message_text(
			chat_id=chat_id,
			message_id=message_id,
			text=text,
			reply_markup=reply_markup
		)
	else:
		await bot.send_message(
			chat_id=chat_id,
			text=text,
			reply_markup=reply_markup
		)
	return content


async def client_help_RegisterGroupStart(id: int, chat_id: int, message_id: int):
	await bot.delete_message(
		chat_id=chat_id,
		message_id=message_id
	)
	await bot.send_message(
		chat_id=id,
		text=mscl_RegisterGroupStart,
		reply_markup=kb_reply_CancelRegistration
	)
	await FSMGroupRegister.name.set()
	content = 'Started group registration.'
	return content


# <---------- Callback функции ---------->
async def client_callback_GroupPanel(query: types.CallbackQuery):
	"""
	Open group panel for user from callback button.
	:param query:
	:return:
	"""
	try:
		content = await client_help_GroupPanel(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			message_id=query.message.message_id
		)
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='client_callback_GroupPanel',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='client_callback_GroupPanel',
			exception=exception,
			content=''
		)


async def client_callback_RegisterGroupStart(query: types.CallbackQuery):
	"""
	Starts group registration FSM machine from callback button.
	:param query:
	:return:
	"""
	try:
		content = await client_help_RegisterGroupStart(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			message_id=query.message.message_id
		)
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='client_callback_RegisterGroupStart',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='client_callback_RegisterGroupStart',
			exception=exception,
			content=''
		)


# <---------- Handler функции ---------->
async def client_handler_CommandStartOrHelp(message: types.Message):
	"""
	Triggered by 'help' command use.
	:param message:
	:return:
	"""
	try:
		exception = ''
		if await client_help_ChatIsGroup(message=message):
			content = 'No database operations.'
			exception = 'Used from group.'
		else:
			client_data = await db_psql_UserData(id=message.from_user.id)
			if client_data['username']:
				if client_data['group_id']:
					text = mscl_CommandStartOrHelp_WithGroup
					reply_markup = kb_reply_CommandStartOrHelp
				else:
					text = mscl_CommandStartOrHelp_NoGroup
					reply_markup = kb_inline_GroupPanel
				content = 'Already on database.'
			else:
				text = await mscl_CommandStartOrHelp_NoRegister(first_name=message.from_user.full_name.split()[0])
				reply_markup = kb_inline_GroupPanel
				response = await db_psql_InsertUser(
					id=message.from_user.id,
					username=message.from_user.username,
					full_name=message.from_user.full_name
				)
				if response:
					content = 'Added to database.'
				else:
					content = 'Failed to add to database.'
			await message.answer(
				text=text,
				reply_markup=reply_markup,
				disable_web_page_preview=True
			)
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_CommandStartOrHelp',
			exception=exception,
			content=f'Initialized {message.text} command. {content}'
		)
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_CommandStartOrHelp',
			exception=exception,
			content=''
		)


async def client_handler_GroupPanel(message: types.Message):
	"""
	Open group panel for user from callback button.
	:param message:
	:return:
	"""
	try:
		if await client_help_ChatIsGroup(message=message):
			exception = 'Used from group.'
			content = ''
		else:
			await message.delete()
			exception = ''
			content = await client_help_GroupPanel(
				id=message.from_user.id,
				chat_id=message.chat.id,
			)
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_GroupPanel',
			exception=exception,
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_GroupPanel',
			exception=exception,
			content=''
		)


async def client_handler_RegisterGroupStart(message: types.Message):
	"""
	Starts group registration FSM machine.
	:param message:
	:return:
	"""
	try:
		if await client_help_ChatIsGroup(message=message):
			exception = 'Used from group.'
			content = ''
		else:
			exception = ''
			content = await client_help_RegisterGroupStart(
				id=message.from_user.id,
				chat_id=message.chat.id,
				message_id=message.message_id
			)
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_RegisterGroupStart',
			exception=exception,
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_RegisterGroupStart',
			exception=exception,
			content=''
		)


async def client_handler_CancelFSM(message: types.Message, state: FSMContext):
	"""
	Cancel active FSM machine.
	:param message:
	:param state:
	:return:
	"""
	try:
		if await client_help_ChatIsGroup(message=message):
			exception = 'Used from group.'
			content = ''
		else:
			current_state = await state.get_state()
			if not current_state:
				text = 'Нечего отменять 🤷'
				exception = 'No active state.'
				content = ''
			else:
				await state.finish()
				text = 'Отменено 👍'
				exception = ''
				content = 'Register'
			await message.answer(
				text=text,
				reply_markup=kb_reply_CommandStartOrHelp
			)
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_RegisterGroupCancel',
			exception=exception,
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_RegisterGroupCancel',
			exception=exception,
			content=''
		)


async def client_handler_RegisterGroupName(message: types.Message, state: FSMContext):
	"""
	Set name for group.
	:param message:
	:param state:
	:return:
	"""
	try:
		pass
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_RegisterGroupPassword',
			exception=exception,
			content=''
		)


def register_handlers():
	"""
	Registration of all message and callback handlers.
	:param dp:
	:return:
	"""
	router.message.register(client_handler_CommandStartOrHelp, Command('start'), filter_ChatType(chat_types=['private']))
	router.message.register(client_handler_GroupPanel, F.text == msreg_GroupPanelMessage, filter_ChatType(chat_types=['private']))
	# dp.register_message_handler(client_handler_GroupPanel, Text(equals=msreg_GroupPanelMessage, ignore_case=True))
	# dp.register_callback_query_handler(client_callback_GroupPanel, Text('GroupPanel'))

	# dp.register_callback_query_handler(client_callback_RegisterGroupStart, Text('CreateGroup'))
	# dp.register_message_handler(client_handler_RegisterGroupStart, Text(equals=msreg_RegistrationGroupStart, ignore_case=True))
	# dp.register_message_handler(client_handler_CancelFSM, Text(equals=msreg_CancelFSM, ignore_case=True), state='*')
