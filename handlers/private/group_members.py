# <---------- Python modules ---------->
from aiogram import types, Router, F


# <---------- Local modules ---------->
from create_bot import bot, psql
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters
from data_base import operations


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
		data = await operations.userData(id=id)
		data_formatted = await operations.userData(id=id, formatted=True)
		if data['group_admin']:
			reply_markup = await kb_private.inline_memberActions(
				id=id,
				for_admin=True
			)
		else:
			reply_markup = await kb_private.inline_memberActions(id=id)
		await callback_query.message.edit_text(
			text=(
				f'<blockquote>{data_formatted}</blockquote>\n\n'
				f'Что хотите сделать с участником?'
			),
			reply_markup=reply_markup
		)
		exception = ''
		content = ''
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
