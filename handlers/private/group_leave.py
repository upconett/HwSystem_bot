# <---------- Python modules ---------->
from aiogram import types, Router, F


# <---------- Local modules ---------->
from create_bot import psql
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'group_leave.py'


# <---------- Main functions ---------->
async def callback_query_leaveGroup(callback_query: types.CallbackQuery):
	"""
	Starts group leaving from callback button.
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		await callback_query.message.edit_text(
			text=ms_private.groupLeave,
			reply_markup=kb_private.inline_leaveGroupConfirm
		)
	except Exception as exc:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			filename=filename,
			function='callback_query_leaveGroup',
			exception=exc,
			content=''
		)


async def message_leaveGroup(message: types.Message):
	try:
		await message.answer(
			text=ms_private.groupLeave,
			reply_markup=kb_private.inline_leaveGroupConfirm
		)
		await message.delete()
	except Exception as exc:
		await ut_logger.create_log(
			id=message.from_user.id,
			filename=filename,
			function='message_leaveGroup',
			exception=exc,
			content=''
		)


async def callback_query_leaveGroupConfirmed(callback_query: types.CallbackQuery):
	try:
		await callback_query.answer()
		await callback_query.message.edit_text(
			text=ms_private.groupLeaved
		)
		await psql.update(
			table='users',
			what='group_id',
			what_value=None,
			where='id',
			where_value=callback_query.from_user.id
		)
	except Exception as exc:
		await ut_logger.create_log(
			id=callback_query.from_user.id,
			filename=filename,
			function='callback_query_leaveGroupConfirm',
			exception=exc,
			content=''
		)


# <---------- Registration handlers ---------->
def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filter ChatType(chat_types=['private'], data_type='message'), UserPresenceInGroup()
	:param router:
	:return:
	"""
	router.callback_query.register(callback_query_leaveGroup, F.data == 'LeaveGroup')
	router.message.register(message_leaveGroup, ut_filters.TextEquals(list_ms=ms_regular.groupLeave, data_type='message'))
	router.callback_query.register(callback_query_leaveGroupConfirmed, F.data == 'LeaveGroupConfirm')
