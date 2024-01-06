# <---------- Python modules ---------->
from aiogram import types, Router, F


# <---------- Local modules ---------->
from create_bot import bot, psql
from data_base import operations
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'commands.py'


# <---------- Start/help commands ---------->
async def message_commandStartOrHelp(message: types.Message):
	"""
	Triggered by 'help' command use.
	:param message:
	:return:
	"""
	try:
		client_data = await operations.userData(id=message.from_user.id)
		if client_data['username']:
			if client_data['group_id']:
				text = ms_private.commandStartOrHelp_forGroupMember
				reply_markup = kb_private.reply_commandStartOrHelp
			else:
				text = ms_private.commandStartOrHelp_forNotGroupMember
				reply_markup = kb_private.inline_groupPanel
			content = 'Already on database.'
		else:
			text = await ms_private.commandStartOrHelp_forNotRegistered(first_name=message.from_user.full_name.split()[0])
			reply_markup = kb_private.inline_groupPanel
			await operations.insertUser(
				id=message.from_user.id,
				username=message.from_user.username,
				full_name=message.from_user.full_name
			)
			content = 'Added to database.'
		await message.answer(
			text=text,
			reply_markup=reply_markup,
			disable_web_page_preview=True
		)
		await ut_logger.create_log(
			id=message.from_user.id,
			filename=filename,
			function='message_commandStartOrHelp',
			exception='',
			content=f'Initialized {message.text} command. {content}'
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=message.from_user.id,
			filename=filename,
			function='message_commandStartOrHelp',
			exception=exception,
			content=''
		)


# <---------- Group panel ---------->
async def groupPanel(id: int, message_id: int = None):
	"""
	Used for callback and message handlers to display the group panel.
	:param id: Telegram ID
	:param message_id: Telegram parent message ID
	:return:
	"""
	data = await operations.userData(id=id)
	if not data['group_id']:
		text = ms_private.groupPanel_forNotMember
		reply_markup = kb_private.inline_groupPanelForNotMember
		content = 'Called the group panel without being a group member.'
	else:
		is_owner = (await psql.select(
			table='groups',
			what='owner_id',
			where='group_id',
			where_value=data['group_id']
		))[0][0]
		if is_owner == id:
			text = ms_private.groupPanel_forOwner
			reply_markup = kb_private.inline_GroupPanelForOwner
			content = 'Called the group panel as the creator of the group.'
		else:
			text = ms_private.groupPanel_forMember
			reply_markup = kb_private.inline_groupPanelForMember
			content = 'Called the group panel as a group member.'
	if message_id:
		await bot.edit_message_text(
			chat_id=id,
			message_id=message_id,
			text=text,
			reply_markup=reply_markup
		)
	else:
		await bot.send_message(
			chat_id=id,
			text=text,
			reply_markup=reply_markup
		)
	return content


async def callback_query_groupPanel(callback_query: types.CallbackQuery):
	"""
	Open group panel for user from callback button.
	:param callback_query:
	:return:
	"""
	try:
		content = await groupPanel(
			id=callback_query.from_user.id,
			message_id=callback_query.message.message_id
		)
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			filename=filename,
			function='callback_query_groupPanel',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			filename=filename,
			function='callback_query_groupPanel',
			exception=exception,
			content=''
		)


async def message_groupPanel(message: types.Message):
	"""
	Open group panel for user from callback button.
	:param message:
	:return:
	"""
	try:
		await message.delete()
		content = await groupPanel(
			id=message.from_user.id
		)
		await ut_logger.create_log(
			id=message.from_user.id,
			filename=filename,
			function='message_groupPanel',
			exception='',
			content=content
		)
	except Exception as exception:
		await ut_logger.create_log(
			id=message.from_user.id,
			filename=filename,
			function='message_groupPanel',
			exception=exception,
			content=''
		)


def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(['private'])
	:param router:
	:return:
	"""
	router.message.register(message_commandStartOrHelp, ut_filters.TextEquals(list_ms=ms_regular.startOrHelp, data_type='message'))
	router.callback_query.register(callback_query_groupPanel, F.data == 'GroupPanel')
	router.message.register(message_groupPanel, ut_filters.TextEquals(list_ms=ms_regular.groupPanel, data_type='message'))
