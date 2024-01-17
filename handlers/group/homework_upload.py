# <---------- Python modules ---------->
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


# <---------- Local modules ---------->
from create_bot import bot
from utilities import ut_logger, ut_handlers
from utilities.ut_handlers import quotate
from data_base import operations
from messages.ms_group import homeworkUpload, homeworkReUpload,\
	homeworkUploadRewrite, homeworkUploadAdd, separateMessage
from keyboards.kb_group import inline_homeworkUpload
from exceptions.ex_handlers import *


# <---------- Variables ---------->
filename = 'homework_upload.py'


# <---------- Finite States Machine ---------->
class UploadHomeworkFSM(StatesGroup):
	hw_mistake = State()
	hw_approve = State()


# <---------- Utility functions ---------->
async def cleanup(messages: list[types.Message]) -> None:
	"""
	Deletes all residual messages after homework has been added.
	:param messages: List of messages (stored in data['messages'])
	:return:
	"""
	chat_id = messages[0].chat.id
	message_ids = [ms.message_id for ms in messages]
	await bot.delete_messages(
		chat_id=chat_id,
		message_ids=message_ids
	)


# <---------- Homework uploading ---------->
async def message_uploadApprove(message: types.Message, state: FSMContext):
	"""
	The last step in HW upload.\n
	Checks if hw is already set and sends confirmation message.\n
	Works with message.\n
	---
	:param message:
	:param state:
	:return:
	"""
	try:
		data = await state.get_data()
		result = await operations.findNextLesson(
			id=message.from_user.id,
			subject=data['subject'],
			date=data['date'],
			weekday=data['weekday']
		)
		if result:
			data['date'] = result['date']
			await state.set_data(data)
			hw = await operations.getHomework(
				id=message.from_user.id,
				date=result['date'],
				subject=data['subject']
			)
			try: data['task']
			except: data['task'] = None
			try: data['photos']
			except: data['photos'] = None
			if not hw or (hw['task'] is None and hw['photos'] is None):
				await operations.setHomework(
					id=message.from_user.id,
					date=result['date'],
					subject=data['subject'],
					task=data['task'],
					photos=data['photos']
				)
				await message.answer(
					text=homeworkUpload(
						date=result['date'],
						subject=data['subject']
					),
					reply_markup=None
				)
			elif data['task'] and hw['photos'] and (not hw['task']):
				await operations.setHomework(
					id=message.from_user.id,
					date=result['date'],
					subject=data['subject'],
					task=data['task'],
					photos=hw['photos']
				)
				await message.answer(
				text=homeworkUploadAdd(
					date=result['date'],
					subject=data['subject']
					),
					reply_markup=None
				)
			elif data['photos'] and hw['task'] and (not data['task']):
				if hw['photos']:
					data['photos'] = hw['photos'] + data['photos']
				await operations.setHomework(
					id=message.from_user.id,
					date=result['date'],
					subject=data['subject'],
					task=hw['task'],
					photos=data['photos']
				)
				await message.answer(
				text=homeworkUploadAdd(
					date=result['date'],
					subject=data['subject']
					),
					reply_markup=None
				)
			else:
				try: data['old_photos'] = hw['photos']
				except: data['old_photos'] = None
				try: data['old_task'] = hw['task']
				except: data['old_task'] = None
				if hw['photos']:
					media_group = [types.InputMediaPhoto(media=i) for i in hw['photos']]
					media_group[0] = types.InputMediaPhoto(
						media=hw['photos'][0],
					 	caption=homeworkUploadRewrite(
							date=result['date'],
							subject=data['subject'],
							hw=hw
						).replace(separateMessage, '')
					)
					data['messages'] = []
					for mess in (await message.answer_media_group(media=media_group)):
						data['messages'].append(mess)
					await message.answer(
						text=(
							'✏️ <b>Добавить</b>\n'
							'🆕 <b>Перезаписать</b>\n'
							'❌ <b>Отменить</b> '
						),
						reply_markup=inline_homeworkUpload
					)
				else:
					await message.answer(
						text=homeworkUploadRewrite(
							date=result['date'],
							subject=data['subject'],
							hw=hw
						),
						reply_markup=inline_homeworkUpload
					)
		await state.set_data(data)
		exception = ''
		content = 'Homework Approval.'
	except SundayException as exc:
		await message.answer(text=exc.alt)
		exception = ''
		content = 'Got SundayException.'
	except NoLessonAtWeekday as exc:
		await message.answer(text=exc.text)
		exception = ''
		content = 'Got NoLessonAtWeekday.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_uploadApprove',
		exception=exception,
		content=content
	)


async def callback_query_uploadApprove(query: types.CallbackQuery, state: FSMContext):
	"""
	The last step in HW upload.\n
	Checks if hw is already set and sends confirmation message.\n
	Works with callback query.\n
	---
	:param query:
	:param state:
	:return:
	"""
	try:
		data = await state.get_data()
		result = await operations.findNextLesson(
			id=query.from_user.id,
			subject=data['subject'],
			date=data['date'],
			weekday=data['weekday']
		)
		if result:
			data['date'] = result['date']
			await state.set_data(data)
			hw = await operations.getHomework(
				id=query.from_user.id,
				date=result['date'],
				subject=data['subject']
			)
			try: data['task']
			except: data['task'] = None
			try: data['photos']
			except: data['photos'] = None
			if not hw or (hw['task'] is None and hw['photos'] is None):
				await operations.setHomework(
					id=query.from_user.id,
					date=result['date'],
					subject=data['subject'],
					task=data['task'],
					photos=data['photos']
				)
				await query.message.edit_text(
				text=homeworkUpload(
					date=result['date'],
					subject=data['subject']
					),
					reply_markup=None
				)
			elif data['task'] and hw['photos'] and (not hw['task']):
				await operations.setHomework(
					id=query.from_user.id,
					date=result['date'],
					subject=data['subject'],
					task=data['task'],
					photos=hw['photos']
				)
				await query.message.edit_text(
				text=homeworkUploadAdd(
					date=result['date'],
					subject=data['subject']
					),
					reply_markup=None
				)
			elif data['photos'] and hw['task'] and (not data['task']):
				if hw['photos']:
					data['photos'] = hw['photos'] + data['photos']
				await operations.setHomework(
					id=query.from_user.id,
					date=result['date'],
					subject=data['subject'],
					task=hw['task'],
					photos=data['photos']
				)
				await query.message.edit_text(
				text=homeworkUploadAdd(
					date=result['date'],
					subject=data['subject']
					),
					reply_markup=None
				)
			else:
				try: data['old_photos'] = hw['photos']
				except: data['old_photos'] = None
				try: data['old_task'] = hw['task']
				except: data['old_task'] = None
				await state.set_data(data)
				if hw['photos']:
					media_group = [types.InputMediaPhoto(media=i) for i in hw['photos']]
					media_group[0] = types.InputMediaPhoto(
						media=hw['photos'][0],
					 	caption=homeworkUploadRewrite(
							date=result['date'],
							subject=data['subject'],
							hw=hw
						).replace(separateMessage, '')
					)
					data['messages'] = []
					for mess in (await query.message.answer_media_group(media=media_group)):
						data['messages'].append(mess)
					await query.message.answer(
						text=(
							'✏️ <b>Добавить</b>\n'
							'🆕 <b>Перезаписать</b>\n'
							'❌ <b>Отменить</b> '
						),
						reply_markup=inline_homeworkUpload
					)
					await query.message.delete()
				else:
					await query.message.edit_text(
						text=homeworkUploadRewrite(
							date=result['date'],
							subject=data['subject'],
							hw=hw	
						),
						reply_markup=inline_homeworkUpload
					)
		await state.set_data(data)
		exception = ''
		content = 'Homework Approval.'
	except SundayException as exc:
		await query.message.delete()
		await query.message.answer(text=exc.alt)
		exception = ''
		content = 'Got SundayException.'
	except NoLessonAtWeekday as exc:
		await query.message.delete()
		await query.message.answer(text=exc.text)
		exception = ''
		content = 'Got NoLessonAtWeekday.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=query.from_user.id,
		filename=filename,
		function='callback_query_uploadApprove',
		exception=exception,
		content=content
	)


async def FSM_callback_query_uploadEdit(query: types.CallbackQuery, state: FSMContext):
	"""
	Upload homework with overwrite.
	:param query:
	:param state:
	:return:
	"""
	try:	
		data = await state.get_data()
		try: data['task']
		except: data['task'] = None
		try: data['photos']
		except: data['photos'] = None
		try:
			await cleanup(data['messages'])
		except:
			pass
		await operations.setHomework(
			id=query.from_user.id,
			date=data['date'],
			subject=data['subject'],
			task=data['task'],
			photos=data['photos']
		)
		if query.message.caption:
			await query.message.delete()
			await query.message.answer(
				text=homeworkReUpload(
					date=data['date'],
					subject=data['subject']
				)
			)
		else:
			await query.message.edit_text(
				text=homeworkReUpload(
					date=data['date'],
					subject=data['subject']
				),
				reply_markup=None
			)
		await state.clear()
		exception = ''
		content = 'User submitted editing upload.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=query.from_user.id,
		filename=filename,
		function='FSM_callback_query_uploadSubmit',
		exception=exception,
		content=content
	)


async def FSM_callback_query_uploadAdd(query: types.CallbackQuery, state: FSMContext):
	"""
	Upload homework as addition to existing.
	:param query:
	:param state:
	:return:
	"""
	try:
		data = await state.get_data()
		for key in ['tasks', 'photos', 'old_task', 'old_photos']:
			try: data[key]
			except: data[key] = None
		if data['old_photos']:
			if data['photos']:
				data['photos'] = data['old_photos'] + data['photos']
			else:
				data['photos'] = data['old_photos']
		if data['old_task'] and data['task']:
			data['task'] = data['old_task'] + "\n\n" + data['task']
		await operations.setHomework(
			id=query.from_user.id,
			date=data['date'],
			subject=data['subject'],
			task=data['task'],
			photos=data['photos']
		)
		try:
			await cleanup(data['messages'])
		except:
			pass
		if query.message.caption:
			await query.message.delete()
			await query.message.answer(
				text=homeworkUploadAdd(
					date=data['date'],
					subject=data['subject']
				)
			)
		else:
			await query.message.edit_text(
				text=homeworkUploadAdd(
					date=data['date'],
					subject=data['subject']
				),
				reply_markup=None
			)
		await state.clear()
		exception = ''
		content = 'User submitted upload.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=query.from_user.id,
		filename=filename,
		function='FSM_callback_query_uploadAdd',
		exception=exception,
		content=content
	)


async def FSM_callback_query_mistakeCorrect(query: types.CallbackQuery, state: FSMContext):
	"""
	Correct mistake in subject naming.
	:param query:
	:param state:
	:return:
	"""
	try:
		data = await state.get_data()
		if data['message_id'] != query.message.message_id:
			await query.answer()
			return
		await state.set_state(UploadHomeworkFSM.hw_approve)
		await callback_query_uploadApprove(
			query=query,
			state=state
		)
		exception = ''
		content = 'User corrected his mistake.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=query.from_user.id,
		filename=filename,
		function='FSM_callback_query_mistakeCorrect',
		exception=exception,
		content=content
	)


async def FSM_callback_query_decline(query: types.CallbackQuery, state: FSMContext):
	"""
	Decline uploading at any state.
	:param query:
	:param state:
	:return:
	"""
	try:
		data = await state.get_data()
		try:
			await cleanup(data['messages'])
		except:
			pass
		await query.message.delete()
		await state.clear()
		exception = ''
		content = 'User declined upload.'
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=query.from_user.id,
		filename=filename,
		function='FSM_callback_query_decline',
		exception=exception,
		content=content
	)


async def FSM_callback_query_dontTouchButtons(query: types.CallbackQuery):
	"""
	For people who tries to press callback buttons while smbd uploads homework.
	:param query:
	:return:
	"""
	await query.answer(
		'Не вы сейчас сохраняете задание!',
		show_alert=True
	)


async def FSM_message_textUpload(message: types.Message, state: FSMContext):
	"""
	Uploading start via keyword.\n
	Working with text (no photos).\n
	---
	:param message:
	:param state:
	:return:
	"""
	try:
		subject, task, weekday, date = await ut_handlers.homeworkExtractDataUpload(message.from_user.id, message.text)
		if task is None:
			raise NoTask
		await state.set_state(UploadHomeworkFSM.hw_approve)
		await state.set_data({
			'id': message.from_user.id,
			'subject': subject,
			'task': task,
			'weekday': weekday,
			'date': date
		})
		await message_uploadApprove(
			message=message,
			state=state
		)
		return
	except NoSubject:
		exception = ''
		content = ''
		pass
	except NoTask as exc:
		await message.answer(exc.text)
		exception = ''
		content = 'User provided no task.'
	except NoMainSchedule as exc:
		await message.answer(exc.text)
		exception = ''
		content = 'Main Schedule is not set.'
	except InvalidSubject as exc:
		await message.answer(
			text=exc.text,
			reply_markup=exc.markup
		)
		if exc.markup:
			await state.set_state(UploadHomeworkFSM.hw_mistake)
			await state.set_data(
				{
					'id': message.from_user.id,
					'message_id': message.message_id + 1,
					'task': exc.task,
					'subject': exc.subject,
					'weekday': exc.weekday, 
					'date': exc.date
				}
			)
		exception = ''
		content = 'User made mistake in subject.'
	except InvalidDate as exc:
		await message.answer(
			text=exc.text,
			parse_mode='MarkdownV2'
		)
		exception = 'InvalidDate'
		content = ''
		await state.clear()
	except TimeTravel as exc:
		await message.answer(
			text=exc.text,
			reply_parameters=quotate(
				message=message,
				quote=exc.quote
			),
			parse_mode='MarkdownV2'
		)
		exception = 'TimeTravel'
		content = ''
		await state.clear()
		ecxeption = ''
		content = 'User Uploaded task'
	except SundayException as exc:
		await message.answer(text=exc.alt)
		exception = 'SundayException'
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_textUpload',
		exception=exception,
		content=content
	)


async def FSM_message_photosUpload(message: types.Message, state: FSMContext):
	"""
	Uploading start via keyword.\n
	Working with photos and captions (no other media allowed).\n
	---
	:param message:
	:param state:
	:return:
	"""
	try:
		if message.photo is None:
			await message.answer(
				text=(
					'<b>Домашнее задание не сохранено</b> ❌\n'
					'Пожалуйста, пришлите <em>сжатое изображение</em> 🙏'
				)
			)
			return
		subject, task, weekday, date = await ut_handlers.homeworkExtractDataUpload(message.from_user.id, message.caption)
		await state.set_state(UploadHomeworkFSM.hw_approve)
		await state.set_data({
			'id': message.from_user.id,
			'subject': subject,
			'task': task,
			'photos': [message.photo[-1].file_id],
			'weekday': weekday,
			'date': date
		})
		await message_uploadApprove(
			message=message,
			state=state
		)
		return
	except NoSubject:
		exception = ''
		content = ''
		pass
	except NoMainSchedule as exc:
		await message.answer(exc.text)
		exception = ''
		content = 'Main Schedule is not set.'
	except InvalidSubject as exc:
		await message.answer(
			text=exc.text,
			reply_markup=exc.markup
		)
		if exc.markup:
			await state.set_state(UploadHomeworkFSM.hw_mistake)
			await state.set_data(
				{
					'id': message.from_user.id,
					'message_id': message.message_id + 1,
					'task': exc.task,
					'photos': [message.photo[-1].file_id],
					'subject': exc.subject,
					'weekday': None,
					'date': None
				}
			)
		exception = ''
		content = 'User made mistake in subject.'
	except InvalidDate as exc:
		await message.answer(
			text=exc.text,
			reply_parameters=quotate(
				message=message,
				quote=exc.quote
			),
			parse_mode='MarkdownV2'
		)
		exception = 'InvalidDate'
		content = ''
		await state.clear()
	except TimeTravel as exc:
		await message.answer(
			text=exc.text,
			reply_parameters=quotate(
				message=message,
				quote=exc.quote
			),
			parse_mode='MarkdownV2'
		)
		exception = 'TimeTravel'
		content = ''
		await state.clear()
	except SundayException as exc:
		await message.answer(text=exc.alt)
		exception = 'SundayException'
		content = ''
	except Exception as exc:
		exception = exc
		content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='FSM_message_photosUpload',
		exception=exception,
		content=content
	)
	

# <---------- Handlers registration ---------->
def register_handlers(router: Router):
	"""
	Registration of all message and callback handlers.
	Use router with filters:
	- message: ChatType(chat_types=['group','supergroup'], data_type='message'), UserPresenceInGroup()
	- callback_query: ChatType(chat_types=['group','supergroup'], data_type='callback_query'), UserPresenceInGroup()
	:param router:
	:return:
	"""
	router.callback_query.register(FSM_callback_query_mistakeCorrect, F.data == 'HomeworkAccept', StateFilter(UploadHomeworkFSM.hw_mistake))
	router.callback_query.register(FSM_callback_query_uploadEdit, F.data == 'HomeworkEdit', StateFilter(UploadHomeworkFSM.hw_approve))
	router.callback_query.register(FSM_callback_query_uploadAdd, F.data == 'HomeworkAdd', StateFilter(UploadHomeworkFSM.hw_approve))
	router.callback_query.register(FSM_callback_query_decline, F.data == 'HomeworkDecline', StateFilter(UploadHomeworkFSM))

	router.callback_query.register(FSM_callback_query_dontTouchButtons, F.data.startswith('Homework'))

	router.message.register(FSM_message_photosUpload, F.caption.lower().startswith(ms_regular.hw_keywords))
	router.message.register(FSM_message_textUpload, F.text.lower().startswith(ms_regular.hw_keywords))