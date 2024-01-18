# <---------- Python modules ---------->
from aiogram import types, Router, F


# <---------- Local modules ---------->
from create_bot import psql
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'group_delete.py'


# <---------- Main functions ---------->
async def callback_query_deleteGroup(callback_query: types.CallbackQuery):
	"""
	Starts group leaving from callback button.
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		await callback_query.message.edit_text(
			text=ms_private.groupDelete,
			reply_markup=kb_private.inline_deleteGroupConfirm
		)
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_deleteGroup',
		exception=exception,
		content=content
	)


async def message_deleteGroup(message: types.Message):
	try:
		await message.answer(
			text=ms_private.groupDelete,
			reply_markup=kb_private.inline_deleteGroupConfirm
		)
		await message.delete()
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_deleteGroup',
		exception=exception,
		content=content
	)


async def callback_query_deleteGroupConfirmed(callback_query: types.CallbackQuery):
	try:
		await callback_query.answer()
		await callback_query.message.edit_text(
			text=ms_private.groupDeleted
		)
		group_id = (await psql.select(
			table='users',
			what='group_id',
			where='id',
			where_value=callback_query.from_user.id
		))[0][0]
		await psql.update(
			table='users',
			what='group_id',
			what_value=None,
			where='group_id',
			where_value=group_id
		)
		for table in ['chats', 'groups']:
			await psql.delete(
				table=table,
				where='group_id',
				where_value=group_id
			)
		exception = ''
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_deleteGroupConfirm',
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
	router.callback_query.register(callback_query_deleteGroup, F.data == 'DeleteGroup')
	router.message.register(message_deleteGroup, ut_filters.TextEquals(list_ms=ms_regular.groupDelete, data_type='message'))
	router.callback_query.register(callback_query_deleteGroupConfirmed, F.data == 'DeleteGroupConfirm')
