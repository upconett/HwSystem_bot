# <---------- Python modules ---------->
from aiogram import types, Router, F


# <---------- Local modules ---------->
from create_bot import bot, psql
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'group_members.py'


# <---------- Main functions ---------->
async def callback_query_groupMembers(callback_query: types.CallbackQuery):
	"""
	Starts group leaving from callback button.
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		page = int(callback_query.data.split('|')[1])
		group_id = (await psql.select(
			table='users',
			what='group_id',
			where='id',
			where_value=callback_query.from_user.id
		))[0][0]
		group_members = await psql.select(
			table='users',
			what='*',
			where='group_id',
			where_value=group_id
		)
		reply_markup, members_amount = await kb_private.inline_members(members=group_members, page=page)
		await callback_query.message.edit_text(
			text=ms_private.groupMembers,
			reply_markup=reply_markup
		)
		content = f'Showed a list of {members_amount} members.'
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_groupMembers',
		exception=exception,
		content=content
	)


async def callback_query_viewMember(callback_query: types.CallbackQuery):
	try:
		await callback_query.answer()
		id = int(callback_query.data.split('|')[1])
		await callback_query.message.edit_text(
			text=''
		)
		exception = ''
		content = f''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_viewMember',
		exception=exception,
		content=content
	)


# <---------- Registration handlers ---------->
def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(chat_types=['private'], data_type='message'), UserPresenceInGroup()
	:param router:
	:return:
	"""
	router.callback_query.register(callback_query_groupMembers, F.data.startswith('ListMembers'))
	router.callback_query.register(callback_query_viewMember, F.data.startswith('GetMember'), F.data != 'GetMember|✖️')
