# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types
from aiogram.types import ContentType
# from aiogram.dispatcher.filters import Text


# <---------- Импорт сторонних функций ---------->
from json import loads


# <---------- Импорт локальных функций ---------->
from create_bot import bot, psql
from data_base.db_psql import *
from messages.ms_group import *
from keyboards.kb_group import *
from utilities.ut_logger import ut_LogCreate
from utilities.ut_security import ut_EncodeLink
from utilities.ut_pyrogrambot import ut_GetChatMembers
from data_base.operation import db_psql_InsertChat, db_psql_UserData


# <---------- Импорт локальных функций ---------->
from json import loads


# <---------- Переменные ---------->
filename = 'group.py'


# <---------- Вспомогательные функции ---------->
async def group_IsChatAdmin(chat_admins: list, id: int) -> bool:
	"""
	Checks if the user is a chat admin.
	:param chat_admins: Get by message.chat.get_administrators()
	:param id: Telegram ID of the user to check
	:return:
	"""
	for user in range(len(chat_admins)):
		if (id == chat_admins[user]['user']['id']) and chat_admins[user]['can_delete_messages'] and chat_admins[user]['can_restrict_members']:
			return True
	return False


# <---------- Callback функции ---------->
async def group_callback_SelectGroup(query: types.CallbackQuery):
	"""
	Changes the initialization welcome message to select groups that can be associated with the chat.
	:param query:
	:return:
	"""
	try:
		await query.answer()
		is_admin = await group_IsChatAdmin(
			chat_admins=(await query.message.chat.get_administrators()),
			id=query.from_user.id
		)
		if is_admin:
			data = await db_psql_UserData(id=query.from_user.id)
			if data['username']:
				group_ids = loads(query.data.split('|')[1])
				group_names = loads((query.data.split('|')[2]).replace("'", '"'))
				groups = [group_ids, group_names]
				await bot.edit_message_text(
					chat_id=query.message.chat.id,
					message_id=query.message.message_id,
					text=msgr_SelectGroup,
					reply_markup=(await kb_inline_SelectGroup(groups=groups))
				)
				content = f'There are this groups: {groups} - in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
			else:
				await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не пользователь бота, а потому не можете взаимодействовать с ним!')
				content = f'Tried to interact with bot in chat with id={query.message.chat.id}, title={query.message.chat.title}, but no register.'
		else:
			await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не админ, а потому не можете настраивать бота в данном чате!')
			content = f'Tried to configure bot in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_SelectGroup',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
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
		await query.answer()
		is_admin = await group_IsChatAdmin(
			chat_admins=(await query.message.chat.get_administrators()),
			id=query.from_user.id
		)
		if is_admin:
			data = await db_psql_UserData(id=query.from_user.id)
			if data['username']:
				group_id = int(query.data.split('|')[1])
				group_name = query.data.split('|')[2]
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
				content = f'Chosen group with id={group_id}'
			else:
				await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не пользователь бота, а потому не можете взаимодействовать с ним!')
				content = f'Tried to interact with bot in chat with id={query.message.chat.id}, title={query.message.chat.title}, but no register.'
		else:
			await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не админ, а потому не можете настраивать бота в данном чате!')
			content = f'Tried to configure bot in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_BindChatSettings',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
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
		await query.answer()
		is_admin = await group_IsChatAdmin(
			chat_admins=(await query.message.chat.get_administrators()),
			id=query.from_user.id
		)
		if is_admin:
			data = await db_psql_UserData(id=query.from_user.id)
			if data['username']:
				group_id = int(query.data.split('|')[1])
				group_name = query.data.split('|')[2]
				notifications = bool(query.data.split('|')[3])
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
			else:
				await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не пользователь бота, а потому не можете взаимодействовать с ним!')
				content = f'Tried to interact with bot in chat with id={query.message.chat.id}, title={query.message.chat.title}, but no register.'
				exception = ''
		else:
			await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не админ, а потому не можете настраивать бота в данном чате!')
			content = f'Tried to configure bot in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
			exception = ''
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_BindGroup',
			content=content,
			exception=exception
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_BindGroup',
			exception=exception,
			content=''
		)


async def group_callback_DeleteLink(query: types.CallbackQuery):
	try:
		await query.answer()
		is_admin = await group_IsChatAdmin(
			chat_admins=(await query.message.chat.get_administrators()),
			id=query.from_user.id
		)
		if is_admin:
			data = await db_psql_UserData(id=query.from_user.id)
			if data['username']:
				group_id = int(query.data.split('|')[1])
				group_name = query.data.split('|')[2]
				await psql.update(
					table='groups',
					what='group_link',
					what_value=None,
					where='group_id',
					where_value=group_id
				)
				text = await msgr_GroupBoundWithoutLink(
					group_name=group_name,
					full_name=query.from_user.full_name,
					username=query.from_user.username
				)
				await bot.edit_message_text(
					text=text,
					chat_id=query.message.chat.id,
					message_id=query.message.message_id
				)
				content = f'Delete group_link for chat with id={query.message.chat.id}, title={query.message.chat.title}.'
			else:
				await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не пользователь бота, а потому не можете взаимодействовать с ним!')
				content = f'Tried to interact with bot in chat with id={query.message.chat.id}, title={query.message.chat.title}, but no register.'
		else:
			await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не админ, а потому не можете настраивать бота в данном чате!')
			content = f'Tried to configure bot in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_BindGroup',
			content=content,
			exception=''
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_DeleteLink',
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
		await query.answer()
		is_admin = await group_IsChatAdmin(
			chat_admins=(await query.message.chat.get_administrators()),
			id=query.from_user.id
		)
		if is_admin:
			data = await db_psql_UserData(id=query.from_user.id)
			if data['username']:
				await bot.send_message(
					chat_id=query.message.chat.id,
					text=msgr_ChatReloaded
				)
				await group_handler_ChatStart(message=query.message)
				content = f'Chat with id={query.message.chat.id}, title={query.message.chat.title} was deleted from chats table.'
			else:
				await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не пользователь бота, а потому не можете взаимодействовать с ним!')
				content = f'Tried to interact with bot in chat with id={query.message.chat.id}, title={query.message.chat.title}, but no register.'
		else:
			await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не админ, а потому не можете настраивать бота в данном чате!')
			content = f'Tried to configure bot in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_ReloadChat',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_ReloadChat',
			exception=exception,
			content=''
		)


async def group_callback_UnlinkGroup(query: types.CallbackQuery):
	"""
	Unlink a chat from a group if there is any group in the chat after the bot enters.
	:param query:
	:return:
	"""
	try:
		await query.answer()
		is_admin = await group_IsChatAdmin(
			chat_admins=(await query.message.chat.get_administrators()),
			id=query.from_user.id
		)
		if is_admin:
			data = await db_psql_UserData(id=query.from_user.id)
			if data['username']:
				group_id = int(query.data.split('|')[1])
				group_name = query.data.split('|')[2]
				await psql.delete(
					table='chats',
					where='group_id',
					where_value=group_id
				)
				text = await msgr_GroupUnlink(group_name=group_name)
				await bot.edit_message_text(
					text=text,
					chat_id=query.message.chat.id,
					message_id=query.message.message_id
				)
				await group_handler_ChatStart(message=query.message)
				content = f'Unlinked chat from group with id={group_id}, name={group_name}.'
			else:
				await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не пользователь бота, а потому не можете взаимодействовать с ним!')
				content = f'Tried to interact with bot in chat with id={query.message.chat.id}, title={query.message.chat.title}, but no register.'
		else:
			await query.message.answer(
				text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не админ, а потому не можете настраивать бота в данном чате!')
			content = f'Tried to configure bot in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_UnlinkGroup',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_UnlinkGroup',
			exception=exception,
			content=''
		)


async def group_callback_ContinueWithGroup(query: types.CallbackQuery):
	"""

	:param query:
	:return:
	"""
	try:
		await query.answer()
		is_admin = await group_IsChatAdmin(
			chat_admins=(await query.message.chat.get_administrators()),
			id=query.from_user.id
		)
		if is_admin:
			data = await db_psql_UserData(id=query.from_user.id)
			if data['username']:
				group_id = int(query.data.split('|')[1])
				group_name = query.data.split('|')[2]
				link = await ut_EncodeLink(
					group_id=group_id,
					id=query.from_user.id
				)
				text = await msgr_GroupBound(group_name=group_name)
				reply_markup = await kb_inline_GroupLink(
					group_id=group_id,
					group_name=group_name,
					link=link
				)
				await PostgreSQL.update(
					self=psql,
					table='groups',
					what='group_link',
					what_value=link,
					where='group_id',
					where_value=group_id
				)
				await bot.edit_message_text(
					chat_id=query.message.chat.id,
					message_id=query.message.message_id,
					text=text,
					reply_markup=reply_markup
				)
				content = f'Chat with id={query.message.chat.id}, title={query.message.chat.title} continue with group with group_id={group_id}, group_name={group_name}.'
			else:
				await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не пользователь бота, а потому не можете взаимодействовать с ним!')
				content = f'Tried to interact with bot in chat with id={query.message.chat.id}, title={query.message.chat.title}, but no register.'
		else:
			await query.message.answer(text=f'<a href="https://t.me/{query.from_user.username}">{query.from_user.full_name}</a>, вы не админ, а потому не можете настраивать бота в данном чате!')
			content = f'Tried to configure bot in chat with id={query.message.chat.id}, title={query.message.chat.title}.'
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_ContinueWithGroup',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_LogCreate(
			id=query.from_user.id,
			chat_id=query.message.chat.id,
			filename=filename,
			function='group_callback_ContinueWithGroup',
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
				bound_group_id = await psql.select(
					table='chats',
					what='group_id',
					where='id',
					where_value=message.chat.id
				)
				if not bound_group_id:
					chat_members = await ut_GetChatMembers(chat_id=message.chat.id)
					if chat_members:
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
						if group_ids and group_names:
							text = msgr_ChatStart
							reply_markup = await kb_inline_ConnectGroup(
								group_ids=group_ids,
								group_names=group_names
							)
							content = f'Bot entered chat with id={message.chat.id}, title={message.chat.title} with this groups: group_ids={group_ids}, group_names={group_names}.'
						else:
							text = msgr_NoGroupsInChat
							reply_markup = kb_inline_ReloadChat
							content = f'Bot entered chat with id={message.chat.id}, title={message.chat.title} without groups.'
					else:
						text = msgr_NoSuperGroup
						reply_markup = None
						content = f'Bot entered non supergroup chat with id={message.chat.id}, title={message.chat.title}.'
				else:
					bound_group_id = bound_group_id[0][0]
					bound_group_name = (await psql.select(
						table='groups',
						what='group_name',
						where='group_id',
						where_value=bound_group_id
					))[0][0]
					text = msgr_BoundChatStart(group_name=bound_group_name)
					reply_markup = await kb_inline_BoundChatStart(
						group_id=bound_group_id,
						group_name=bound_group_name
					)
					content = f'Bot entered chat with id={message.chat.id}, title={message.chat.title} and already linked group with group_id={bound_group_id}, name={bound_group_name}.'
				await bot.send_message(
					chat_id=message.chat.id,
					text=text,
					reply_markup=reply_markup
				)
				await ut_LogCreate(
					id=00000000,
					chat_id=message.chat.id,
					filename=filename,
					function='group_handler_ChatStart',
					exception='',
					content=content
				)
			elif message.from_user.is_bot:
				await bot.send_message(
					chat_id=message.chat.id,
					text=msgr_NewBotInChat
				)
				await ut_LogCreate(
					id=00000000,
					chat_id=message.chat.id,
					filename=filename,
					function='group_handler_ChatStart',
					exception='',
					content=f'Bot greeted other bot with id={message.from_user.bot.id}.'
				)
	except Exception as exception:
		await ut_LogCreate(
			id=00000000,
			chat_id=message.chat.id,
			filename=filename,
			function='group_handler_ChatStart',
			exception=exception,
			content=''
		)


def register_handlers_group(dp: Dispatcher):
	"""

	:param dp:
	:return:
	"""
	# dp.register_message_handler(group_handler_ChatStart, content_types=ContentType.NEW_CHAT_MEMBERS)
	# dp.register_callback_query_handler(group_callback_SelectGroup, Text(startswith='ConnectGroup'))
	# dp.register_callback_query_handler(group_callback_BindChatSettings, Text(startswith='ChosenGroup'))
	# dp.register_callback_query_handler(group_callback_BindGroup, Text(startswith='ChatSettings'))
	# dp.register_callback_query_handler(group_callback_ReloadChat, Text(startswith='ReloadChat'))
	# dp.register_callback_query_handler(group_callback_DeleteLink, Text(startswith='DeleteLink'))
	# dp.register_callback_query_handler(group_callback_UnlinkGroup, Text(startswith='UnlinkGroup'))