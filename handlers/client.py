# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


# <---------- Импорт локальных функций ---------->
from create_bot import bot
from data_base.operation import db_psql_UserData, db_psql_InsertUser
from messages.ms_client import *
from messages.ms_regular import *
from keyboards.kb_client import *
from utilities.ut_logger import ut_LogCreate


# <---------- Переменные ---------->
filename = 'client.py'


# <---------- Машины состояния ---------->
class FSMGroupRegister(StatesGroup):
	name = State()
	password = State()


# <---------- Вспомогательные функции ---------->


# <---------- Callback функции ---------->
async def client_callback_GroupPanel(query: types.CallbackQuery):
	"""

	:param query:
	:return:
	"""
	try:
		data = await db_psql_UserData(id=query.from_user.id)
		if not data['group_id']:
			await bot.edit_message_text(
				chat_id=query.message.chat.id,
				message_id=query.message.message_id,
				text=mscl_GroupPanel_NoGroup,
				reply_markup=kb_inline_GroupVars
			)
		else:
			await bot.edit_message_text(
				chat_id=query.message.chat.id,
				message_id=query.message.message_id,
				text=mscl_GroupPanel_WithGroupNoAdmin
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
	Starts group registration FSM machine.
	:param query:
	:return:
	"""
	try:
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=mscl_RegistergroupStart,
			reply_markup=kb_reply_CancelRegistration
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
		if message.chat.type == 'supergroup' or message.chat.type == 'group':
			await bot.send_message(
				chat_id=message.from_user.id,
				text=f'{message.text} можно использовать только в личных сообщениях!',
				reply_markup=kb_reply_CommandStartOrHelp
			)
			await message.delete()
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
			await bot.send_message(
				chat_id=id,
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


def register_handlers_client(dp: Dispatcher):
	"""
	Регистрация всех message и callback хендлеров.
	:param dp:
	:return:
	"""
	dp.register_message_handler(client_handler_CommandStartOrHelp, Text(equals=msreg_StartOrHelp, ignore_case=True))
