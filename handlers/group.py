# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types
from aiogram.types import ContentType
from aiogram.dispatcher.filters import Text


# <---------- Импорт локальных функций ---------->
from create_bot import bot
from data_base.db_psql import *
from messages.ms_group import *
from keyboards.kb_group import *
from utilities.ut_logger import ut_LogCreate
from utilities.ut_pyrogrambot import ut_GetChatMembers


# <---------- Переменные ---------->
filename = 'group.py'


# <---------- Callback функции ---------->
async def group_callback_SelectGroup(query: types.CallbackQuery):
	pass


# <---------- Handler функции ---------->
async def group_handler_ChatStart(message: types.Message):
	try:
		if message.chat.type == 'group' or message.chat.type == 'supergroup':
			if message.from_user.bot.id == await bot.get_me():
				chat_members = await ut_GetChatMembers(chat_id=message.chat.id)
				groups = []
				for id in chat_members:
					group_id = await PostgreSQL.select(
						table='users',
						what='group_id',
						where='id',
						where_value=id
					)
					group_name = await PostgreSQL.select(
					        table='groups',
						what='group_name',
						where='group_id',
						where_value=group_id
					)
                                        groups.append((group_id, group_name,))
				await bot.send_message(
					chat_id=message.chat.id,
					text=msgr_ChatStart,
					reply_markup=kb_inline_connectGroup(groups)
				)
				await ut_LogCreate(
					id=00000000,
					filename=filename,
					function='group_handler_ChatStart',
					exception='',
					content=f'Bot entered chat with id={message.chat.id}, title={message.chat.title}.'
				)
			elif message.from_user.is_bot:
				await bot.send_message(
					chat_id=message.chat.id,
					text=msgr_NewBotInChat
				)
				await ut_LogCreate(
					id=00000000,
					filename=filename,
					function='group_handler_ChatStart',
					exception='',
					content=f'Bot greeted other bot with id={message.from_user.bot.id}.'
				)
	except Exception as exception:
		await ut_LogCreate(
			id=00000000,
			filename=filename,
			function='group_handler_ChatStart',
			exception=exception,
			content=''
		)


def register_handlers_group(dp: Dispatcher):
	dp.register_message_handler(group_handler_ChatStart, content_types=ContentType.NEW_CHAT_MEMBERS)
	dp.register_callback_query_handler(group_callback_SelectGroup, Text(startswith='ConnectGroup'))
