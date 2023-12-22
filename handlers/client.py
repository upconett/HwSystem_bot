# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


# <---------- Импорт локальных функций ---------->
from create_bot import bot
from data_base.operation import db_psql_UserData, db_psql_InsertUser
from messages.ms_client import *
from messages.ms_regular import *
from keyboards.kb_client import *
from utilities.ut_logger import ut_LogCreate


# <---------- Переменные ---------->
filename = 'client.py'


# <---------- Вспомогательные функции ---------->
async def client_support_CommandStartOrHelp(id: int, full_name: str, username: str):
	"""
	Unified function for 'help' command or 'ButtonHelp' callback.
	:param id: Telegram ID
	:param full_name: Full name from Telegram
	:param username: Username from Telegram
	:return: content - result of operations with PostgreSQL
	"""
	client_data = await db_psql_UserData(id=id)
	if client_data['username']:
		if client_data['group_id']:
			text = mscl_CommandStartOrHelp_WithGroup
			reply_markup = kb_reply_CommandStartOrHelp
		else:
			text = mscl_CommandStartOrHelp_NoGroup
			reply_markup = kb_inline_GroupPanel
		content = 'Already on database.'
	else:
		text = await mscl_CommandStartOrHelp_NoRegister(first_name=full_name.split()[0])
		reply_markup = kb_inline_GroupPanel
		response = await db_psql_InsertUser(
			id=id,
			username=username,
			full_name=full_name
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
	return content


# <---------- Callback функции ---------->
async def client_callback_CommandStartOrHelp(query: types.CallbackQuery):
	"""
	Triggered by 'ButtonHelp' callback use.
	:param query:
	:return:
	"""
	try:
		content = await client_support_CommandStartOrHelp(
			id=query.from_user.id,
			full_name=query.from_user.full_name,
			username=query.from_user.username
		)
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='client_callback_CommandStartOrHelp',
			exception='',
			content=f'Initialized {query.data} callback. {content}'
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='client_callback_CommandStartOrHelp',
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
			content = await client_support_CommandStartOrHelp(
				id=message.from_user.id,
				full_name=message.from_user.full_name,
				username=message.from_user.username
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
	dp.register_callback_query_handler(client_callback_CommandStartOrHelp, Text('ButtonHelp'))
