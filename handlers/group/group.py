# <---------- Python modules ---------->
from aiogram import Router, types, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from json import loads


# <---------- Local modules ---------->
from create_bot import bot, psql
from messages import ms_group
from keyboards import kb_group
from utilities import ut_logger, ut_security, ut_pyrogrambot, ut_filters
from data_base import operations


# <---------- Variables ---------->
filename = 'group.py'


# <---------- Chat start ---------->
async def message_chatStart(message: types.Message):
	try:
		await bot.send_message(
			chat_id=message.chat.id,
			text=ms_group.chatFirstMessage,
			reply_markup=kb_group.inline_firstMessage
		)
		await ut_logger.create_log(
			id=00000000,
			chat_id=message.chat.id,
			filename=filename,
			function='message_chatStart',
			exception='',
			content='Bot entered chat.'
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=00000000,
			chat_id=message.chat.id,
			filename=filename,
			function='message_chatStart',
			exception=exception,
			content=''
		)


async def callback_query_chatStart(callback_query: types.CallbackQuery):
	"""
	Activated by a message about a new participant joining the chat; if it is a bot or a user, then we welcome him.
	If the bot sees that it has been added to the chat, it begins the procedure of linking the chat to the group.
	Use router with filter ChatType(['group', 'supergroup'])
	:param callback_query:
	:return:
	"""
	try:
		if callback_query.from_user.bot.id == (await bot.get_me()).id:
			bound_group_id = await psql.select(
				table='chats',
				what='group_id',
				where='id',
				where_value=callback_query.message.chat.id
			)
			if not bound_group_id:
				chat_members = await ut_pyrogrambot.getChatMembers(chat_id=callback_query.message.chat.id)
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
						if group_id:
							if group_id[0][0] and (group_id[0][0] not in group_ids):
								group_name = await psql.select(
									table='groups',
									what='group_name',
									where='group_id',
									where_value=group_id[0][0]
								)
								group_ids.append(group_id[0][0])
								group_names.append(group_name[0][0])
					if group_ids and group_names:
						text = ms_group.chatStart
						reply_markup = await kb_group.inline_chatStart(
							group_ids=group_ids,
							group_names=group_names
						)
						content = f'Bot started chat with this groups: group_ids={group_ids}, group_names={group_names}.'
					else:
						text = ms_group.chatStart_noGroups
						reply_markup = kb_group.inline_reloadChat
						content = f'Bot started chat without groups.'
				else:
					text = ms_group.chatStart_notSupergroup
					reply_markup = None
					content = f'Bot started non supergroup chat.'
			else:
				bound_group_id = bound_group_id[0][0]
				bound_group_name = (await psql.select(
					table='groups',
					what='group_name',
					where='group_id',
					where_value=bound_group_id
				))[0][0]
				text = await ms_group.chatStart_withBoundGroup(group_name=bound_group_name)
				reply_markup = await kb_group.inline_chatStart_withBoundGroup(
					group_id=bound_group_id,
					group_name=bound_group_name
				)
				content = f'Bot entered chat which already linked with group.'
			await bot.send_message(
				chat_id=callback_query.message.chat.id,
				text=text,
				reply_markup=reply_markup
			)
			await ut_logger.create_log(
				id=00000000,
				chat_id=callback_query.message.chat.id,
				filename=filename,
				function='callback_query_chatStart',
				exception='',
				content=content
			)
		elif callback_query.from_user.is_bot:
			await bot.send_message(
				chat_id=callback_query.message.chat.id,
				text=ms_group.newBotInChat
			)
			await ut_logger.create_log(
				id=00000000,
				chat_id=callback_query.message.chat.id,
				filename=filename,
				function='callback_query_chatStart',
				exception='',
				content=f'Bot greeted other bot with id={callback_query.from_user.bot.id}.'
			)
	except Exception as exception:
		await ut_logger.create_log(
			id=00000000,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_chatStart',
			exception=exception,
			content=''
		)


async def callback_query_unlinkGroup(callback_query: types.CallbackQuery):
	"""
	Unlink a chat from a group if there is any group in the chat after the bot enters.
	Use router with filters ChatType(chat_types=['group', 'supergroup']), UserIsChatAdmin(flag=True), UserPresenceInGroup(flag=True)
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		group_id = int(callback_query.data.split('|')[1])
		group_name = callback_query.data.split('|')[2]
		text = await ms_group.unlinkGroup(group_name=group_name)
		await bot.edit_message_text(
			text=text,
			chat_id=callback_query.message.chat.id,
			message_id=callback_query.message.message_id
		)
		await message_chatStart(message=callback_query.message)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_unlinkGroup',
			exception='',
			content=f'Unlinked chat from group.'
		)
		await psql.delete(
			table='chats',
			where='group_id',
			where_value=group_id
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_unlinkGroup',
			exception=exception,
			content=''
		)


async def callback_query_continueWithGroup(callback_query: types.CallbackQuery):
	"""
	Continuation of the bot`s work in chat with a previously linked group.
	Use router with filters ChatType(chat_types=['group', 'supergroup']), UserIsChatAdmin(flag=True), UserPresenceInGroup(flag=True)
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		group_id = int(callback_query.data.split('|')[1])
		group_name = callback_query.data.split('|')[2]
		link = await ut_security.encodeLink(
			group_id=group_id,
			id=callback_query.from_user.id
		)
		await psql.update(
			table='groups',
			what='group_link',
			what_value=link,
			where='group_id',
			where_value=group_id
		)
		text = await ms_group.boundGroup_withLink(group_name=group_name)
		reply_markup = await kb_group.inline_boundGroup(
			group_id=group_id,
			group_name=group_name,
			link=link
		)
		await bot.edit_message_text(
			chat_id=callback_query.message.chat.id,
			message_id=callback_query.message.message_id,
			text=text,
			reply_markup=reply_markup
		)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_continueWithGroup',
			exception='',
			content='Chat continue with specified group.'
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_continueWithGroup',
			exception=exception,
			content=''
		)


# <---------- Bind group to chat ---------->
async def callback_query_selectGroup(callback_query: types.CallbackQuery):
	"""
	Changes the initialization welcome message to select groups that can be associated with the chat.
	Use router with filters ChatType(chat_types=['group', 'supergroup']), UserIsChatAdmin(flag=True), UserPresenceInGroup(flag=True)
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		group_ids = loads(callback_query.data.split('|')[1])
		group_names = loads((callback_query.data.split('|')[2]).replace("'", '"'))
		groups = [group_ids, group_names]
		reply_markup = await kb_group.inline_selectGroup(groups=groups)
		await bot.edit_message_text(
			chat_id=callback_query.message.chat.id,
			message_id=callback_query.message.message_id,
			text=ms_group.selectGroup,
			reply_markup=reply_markup
		)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_selectGroup',
			exception='',
			content=f'There are this groups: {groups}.'
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_selectGroup',
			exception=exception,
			content=''
		)


async def callback_query_bindChatSettings(callback_query: types.CallbackQuery):
	"""
	Changes the message selecting groups to choose whether to enable or disable notifications for the chat.
	Use router with filters ChatType(chat_types=['group', 'supergroup']), UserIsChatAdmin(flag=True), UserPresenceInGroup(flag=True)
	:param callback_query:
	:return:
	"""
	try:
		group_id = int(callback_query.data.split('|')[1])
		group_name = callback_query.data.split('|')[2]
		reply_markup = await kb_group.inline_bindChatSettings(
			group_id=group_id,
			group_name=group_name
		)
		await bot.edit_message_text(
			chat_id=callback_query.message.chat.id,
			message_id=callback_query.message.message_id,
			text=ms_group.bindChatSettings,
			reply_markup=reply_markup
		)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_bindChatSettings',
			exception='',
			content=f'Chosen group with id={group_id}'
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_bindChatSettings',
			exception=exception,
			content=''
		)


async def callback_query_bindGroup(callback_query: types.CallbackQuery):
	"""
	Finally adds the chat to the database with the selected settings and associates it with the specified group.
	Use router with filters ChatType(chat_types=['group', 'supergroup']), UserIsChatAdmin(flag=True), UserPresenceInGroup(flag=True)
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		group_id = int(callback_query.data.split('|')[1])
		group_name = callback_query.data.split('|')[2]
		notifications = bool(callback_query.data.split('|')[3])
		await operations.insertChat(
			id=callback_query.message.chat.id,
			title=callback_query.message.chat.title,
			group_id=group_id,
			notifications=notifications
		)
		link = await ut_security.encodeLink(
			group_id=group_id,
			id=callback_query.from_user.id
		)
		await psql.update(
			table='groups',
			what='group_link',
			what_value=link,
			where='group_id',
			where_value=group_id
		)
		text = await ms_group.boundGroup_withLink(group_name=group_name)
		reply_markup = await kb_group.inline_boundGroup(
			group_id=group_id,
			group_name=group_name,
			link=link
		)
		await bot.edit_message_text(
			chat_id=callback_query.message.chat.id,
			message_id=callback_query.message.message_id,
			text=text,
			reply_markup=reply_markup
		)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='group_callback_bindGroup',
			content='Chat bound to specified group.',
			exception=''
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='group_callback_bindGroup',
			exception=exception,
			content=''
		)


async def callback_query_deleteLink(callback_query: types.CallbackQuery):
	"""
	Removes the link to quickly join the group.
	Use router with filters ChatType(chat_types=['group', 'supergroup']), UserIsChatAdmin(flag=True), UserPresenceInGroup(flag=True)
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		group_id = int(callback_query.data.split('|')[1])
		group_name = callback_query.data.split('|')[2]
		await psql.update(
			table='groups',
			what='group_link',
			what_value=None,
			where='group_id',
			where_value=group_id
		)
		text = await ms_group.boundGroup_withoutLink(
			group_name=group_name,
			full_name=callback_query.from_user.full_name,
			username=callback_query.from_user.username
		)
		await bot.edit_message_text(
			text=text,
			chat_id=callback_query.message.chat.id,
			message_id=callback_query.message.message_id
		)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_deleteLink',
			content='Delete group_link for chat.',
			exception=''
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_deleteLink',
			exception=exception,
			content=''
		)


async def callback_query_reloadChat(callback_query: types.CallbackQuery):
	"""
	Restart linking bot to chat and group.
	Use router with filters ChatType(chat_types=['group', 'supergroup']), UserIsChatAdmin(flag=True), UserPresenceInGroup(flag=True)
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		await bot.send_message(
			chat_id=callback_query.message.chat.id,
			text=ms_group.chatReloaded
		)
		await message_chatStart(message=callback_query.message)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_reloadChat',
			exception='',
			content='Chat was deleted from chats table.'
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			chat_id=callback_query.message.chat.id,
			filename=filename,
			function='callback_query_reloadChat',
			exception=exception,
			content=''
		)


def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(chat_types=['group', 'supergroup'])
	:param router:
	:return:
	"""
	router.my_chat_member.register(message_chatStart, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))

	router.message(ut_filters.BotIsAdministrator(flag=True))

	router.callback_query.register(callback_query_chatStart, F.data == 'StartChat')

	router.message(ut_filters.UserIsChatAdmin(flag=True), ut_filters.UserPresenceInGroup(flag=True), ut_filters.ChatType(['group', 'supergroup']))

	router.callback_query.register(callback_query_unlinkGroup, F.data.startswith('UnlinkGroup'))
	router.callback_query.register(callback_query_continueWithGroup, F.data.startswith('ContinueWithGroup'))
	router.callback_query.register(callback_query_selectGroup, F.data.startswith('Groups'))
	router.callback_query.register(callback_query_bindChatSettings, F.data.startswith('BindGroup'))
	router.callback_query.register(callback_query_bindGroup, F.data.startswith('ChatSettings'))
	router.callback_query.register(callback_query_deleteLink, F.data.startswith('DeleteLink'))
	router.callback_query.register(callback_query_reloadChat, F.data.startswith('ReloadChat'))
