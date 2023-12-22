# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


# <---------- Импорт локальных функций ---------->
from create_bot import bot, psql
from data_base.db_psql import *
from messages.ms_group import *
from keyboards.kb_group import *
from utilities.ut_logger import ut_LogCreate
from utilities.ut_security import ut_EncodeLink
from utilities.ut_pyrogrambot import ut_GetChatMembers
from data_base.operation import db_psql_InsertChat


# <---------- Импорт локальных функций ---------->
from json import loads


# <---------- Переменные ---------->
filename = 'group.py'


# <---------- Callback функции ---------->
async def group_callback_SelectGroup(query: types.CallbackQuery):
	"""
	Changes the initialization welcome message to select groups that can be associated with the chat.
	:param query:
	:return:
	"""
	try:
		group_ids = loads(query.data.split('|')[1])
		group_names = loads((query.data.split('|')[2]).replace("'", '"'))
		groups = [group_ids, group_names]
		print(group_ids, group_names)
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=msgr_SelectGroup,
			reply_markup=(await kb_inline_SelectGroup(groups=groups))
		)
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_SelectGroup',
			exception='',
			content=f'There are this groups: {groups}.'
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_SelectGroup',
			exception=exception,
			content=''
		)


async def group_callback_BindChatSettings(query: types.CallbackQuery):
	"""
	Changes the message selecting groups to choose whether to enable or disable notifications for the chat.
	:param query:
	:return:
	"""
	try:
		group = query.data.split('|')
		group_id = int(group[1])
		group_name = group[2]
		reply_markup = await kb_inline_ChatSettings(
			group_id=group_id,
			group_name=group_name
		)
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=msgr_ChatSettings,
			reply_markup=reply_markup
		)
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_BindChatSettings',
			exception='',
			content=f'Chosen group with id={group[1]}'
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_BindChatSettings',
			exception=exception,
			content=''
		)


async def group_callback_BindGroup(query: types.CallbackQuery):
	"""
	Finally adds the chat to the database with the selected settings and associates it with the specified group.
	:param query:
	:return:
	"""
	try:
		group = query.data.split('|')
		group_id = int(group[1])
		group_name = group[2]
		notifications = bool(group[3])
		response = await db_psql_InsertChat(
			id=query.message.chat.id,
			title=query.message.chat.title,
			group_id=group_id,
			notifications=notifications,
		)
		content = ''
		exception = ''
		if response:
			link = await ut_EncodeLink(
				group_id=group_id,
				id=query.from_user.id
			)
			await PostgreSQL.update(
				self=psql,
				table='groups',
				what='group_link',
				what_value=link,
				where='group_id',
				where_value=group_id
			)
			text = await msgr_GroupBound(group_name=group_name)
			reply_markup = await kb_inline_GroupLink(
				group_id=group_id,
				group_name=group_name,
				link=link
			)
			content = f'Chat with id={query.message.chat.id}, title={query.message.chat.title} bound to group with group_id={group_id}, group_name={group_name}.'
		else:
			text = msgr_GroupBindError
			reply_markup = kb_inline_ReloadChat
			exception = f'Can`t bind chat with id={query.message.chat.id}, title={query.message.chat.title} to group with group_id={group_id}, group_name={group_name}.'
		await bot.edit_message_text(
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			text=text,
			reply_markup=reply_markup
		)
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_BindGroup',
			content=content,
			exception=exception
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_BindGroup',
			exception=exception,
			content=''
		)


async def group_callback_ReloadChat(query: types.CallbackQuery):
	"""
	If an error occurs when linking a chat, the bot starts re-linking (when you press a special button).
	:param query:
	:return:
	"""
	try:
		response = await PostgreSQL.delete(
			self=psql,
			table='chats',
			where='id',
			where_value=query.message.chat.id
		)
		content = ''
		exception = ''
		if response:
			await bot.send_message(
				chat_id=query.message.chat.id,
				text=msgr_ChatReloaded
			)
			await group_handler_ChatStart(message=query.message)
			content = f'Chat with id={query.message.chat.id}, title={query.message.chat.title} was deleted from chats table.'
		else:
			await bot.send_message(
				chat_id=query.message.chat.id,
				text=msgr_ChatReloadError
			)
			exception = f'Can`t delete chat with id={query.message.chat.id}, title={query.message.chat.title} from chats table.'
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_ReloadChat',
			exception=exception,
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			filename=filename,
			function='group_callback_ReloadChat',
			exception=exception,
			content=''
		)


# <---------- Handler функции ---------->
async def group_handler_ChatStart(message: types.Message):
	"""
	Activated by a message about a new participant joining the chat; if it is a bot or a user, then we welcome him.
	If the bot sees that it has been added to the chat, it begins the procedure of linking the chat to the group.
	:param message:
	:return:
	"""
	try:
		if message.chat.type == 'group' or message.chat.type == 'supergroup':
			if message.from_user.bot.id == (await bot.get_me())['id']:
				chat_members = await ut_GetChatMembers(chat_id=message.chat.id)
				group_ids = []
				group_names = []
				for id in chat_members:
					group_id = await psql.select(
						table='users',
						what='group_id',
						where='id',
						where_value=id
					)
					if group_id and (group_id not in group_ids):
						group_name = await psql.select(
							table='groups',
							what='group_name',
							where='group_id',
							where_value=group_id[0][0]
						)
						group_ids.append(group_id[0][0])
						group_names.append(group_name[0][0])
				print(group_ids, group_names)
				reply_markup = await kb_inline_ConnectGroup(
					group_ids=group_ids,
					group_names=group_names
				)
				await bot.send_message(
					chat_id=message.chat.id,
					text=msgr_ChatStart,
					reply_markup=reply_markup
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
	dp.register_message_handler(group_handler_ChatStart, commands='group')  # , content_types=ContentType.NEW_CHAT_MEMBERS
	dp.register_callback_query_handler(group_callback_SelectGroup, Text(startswith='ConnectGroup'))
	dp.register_callback_query_handler(group_callback_BindChatSettings, Text(startswith='ChosenGroup'))
	dp.register_callback_query_handler(group_callback_BindGroup, Text(startswith='ChatSettings'))
	dp.register_callback_query_handler(group_callback_ReloadChat, Text(startswith='ReloadChat'))
