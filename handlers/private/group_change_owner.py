# <---------- Python modules ---------->
from aiogram import types, Router, F


# <---------- Local modules ---------->
from create_bot import bot, psql
from messages import ms_private, ms_regular
from keyboards import kb_private
from utilities import ut_logger, ut_filters


# <---------- Variables ---------->
filename = 'group_change_owner.py'


# <---------- Side functions ---------->
async def side_changeOwnerGroup(id: int, message_id: int = None):
	group_id = (await psql.select(
		table='users',
		what='group_id',
		where='id',
		where_value=id
	))[0][0]
	group_admins_uf = await psql.select_two(
		table='users',
		what='id',
		where='group_id',
		where_value=group_id,
		where_2='group_admin',
		where_value_2=True
	)
	if group_admins_uf:
		group_admins = []
		for admin_id in group_admins_uf:
			if admin_id[0] == id:
				continue
			group_admins.append(admin_id[0])
		reply_markup = await kb_private.inline_groupAdmins(group_admins=group_admins)
		if message_id:
			await bot.edit_message_text(
				chat_id=id,
				message_id=message_id,
				text=ms_private.groupAdmins,
				reply_markup=reply_markup.as_markup()
			)
		else:
			await bot.send_message(
				chat_id=id,
				text=ms_private.groupAdmins,
				reply_markup=reply_markup.as_markup()
			)
		content = 'Showed a list of admins.'
	else:
		if message_id:
			await bot.edit_message_text(
				chat_id=id,
				message_id=message_id,
				text=ms_private.groupNoAdmins
			)
		else:
			await bot.send_message(
				chat_id=id,
				text=ms_private.groupNoAdmins
			)
		content = 'No admins.'
	return content


# <---------- Main functions ---------->
async def callback_query_changeOwnerGroup(callback_query: types.CallbackQuery):
	"""
	Starts group leaving from callback button.
	:param callback_query:
	:return:
	"""
	try:
		await callback_query.answer()
		content = await side_changeOwnerGroup(id=callback_query.from_user.id, message_id=callback_query.message.message_id)
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_changeOwnerGroup',
		exception=exception,
		content=content
	)


async def message_changeOwnerGroup(message: types.Message):
	try:
		await message.delete()
		content = await side_changeOwnerGroup(id=message.from_user.id)
		exception = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_changeOwnerGroup',
		exception=exception,
		content=content
	)


async def callback_query_changeOwnerGroupConfirm(callback_query: types.CallbackQuery):
	try:
		await callback_query.answer()
		id = int(callback_query.data.split('|')[1])
		name = callback_query.data.split('|')[2]
		text = await ms_private.groupConfirmNewOwner(name=name)
		reply_markup = await kb_private.inline_confirmNewOwner(id=id)
		await callback_query.message.edit_text(
			text=text,
			reply_markup=reply_markup
		)
		exception = ''
		content = f'Chosen admin with id={id}.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_changeOwnerGroupConfirm',
		exception=exception,
		content=content
	)


async def callback_query_changeOwnerGroupConfirmed(callback_query: types.CallbackQuery):
	try:
		await callback_query.answer()
		id = int(callback_query.data.split('|')[1])
		await callback_query.message.edit_text(text=ms_private.groupNewOwner)
		await psql.update(
			table='groups',
			what='owner_id',
			what_value=id,
			where='owner_id',
			where_value=callback_query.from_user.id
		)
		await psql.update(
			table='users',
			what='group_admin',
			what_value=True,
			where='id',
			where_value=callback_query.from_user.id
		)
		await psql.update(
			table='users',
			what='group_admin',
			what_value=False,
			where='id',
			where_value=id
		)
		await bot.send_message(
			chat_id=id,
			text=ms_private.groupToNewOwner,
			reply_markup=kb_private.reply_commandStartOrHelp
		)
		exception = ''
		content = f'Admin with id={id} appointed.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=callback_query.from_user.id,
		filename=filename,
		function='callback_query_changeOwnerGroupConfirmed',
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
	router.callback_query.register(callback_query_changeOwnerGroup, F.data == 'ChangeOwner')
	router.message.register(message_changeOwnerGroup, ut_filters.TextEquals(list_ms=ms_regular.groupChangeOwner, data_type='message'))
	router.callback_query.register(callback_query_changeOwnerGroupConfirm, F.data.startswith('ChangeOwnerTo'))
	router.callback_query.register(callback_query_changeOwnerGroupConfirmed, F.data.startswith('ConfirmNewOwner'))
