# <---------- Python modules ---------->
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import json

# <---------- Local modules ---------->
from create_bot import bot
from utilities import ut_logger, ut_handlers
from data_base import operations
from messages.ms_private import homeworkUpload, homeworkReUpload,\
	homeworkUploadRewrite
from exceptions.ex_handlers import *

# <---------- Variables ---------->
filename = 'homework_upload.py'


# <---------- Finite State Machine ---------->
class UploadHomeworkFSM(StatesGroup):
	hw_mistake = State()
	hw_approve = State()


# <---------- Homework uploading ---------->
async def UploadApprove(state: FSMContext, message: types.Message = None, query: types.CallbackQuery = None):
	try:
		data = await state.get_data()
		if message:
			id = message.from_user.id
		else:
			id = query.from_user.id
		result = await operations.findNextLesson(
			id=id,
			subject=data['subject'],
			date=data['date'],
			weekday=data['weekday']
		)
		if result:
			data['date'] = result['date']
			data['weekday'] = result['weekday']
			await state.set_data(data)
			hw = await operations.getHomework(
				id=id,
				date=result['date'],
				subject=data['subject']
			)
			if not hw or (hw['task'] is None and hw['photo'] is None):
				try: data['task']
				except: data['task'] = None
				try: data['photo']
				except: data['photo'] = None
				await operations.setHomework(
					id=id,
					date=result['date'],
					subject=data['subject'],
					task=data['task'],
					photo=data['photo']
				)
				if message:
					await message.answer(
						text=await homeworkUpload(
							date=result['date'],
							subject=data['subject']
						),
						reply_markup=None
					)
				else:
					await query.message.edit_text(
						text=await homeworkUpload(
							date=result['date'],
							subject=data['subject']
						),
						reply_markup=None
					)
			else:
				if hw['photo']:
					if message:
						await message.answer_photo(
							photo=hw['photo'],
							caption=await homeworkUploadRewrite(
								date=result['date'],
								subject=data['subject'],
								hw=hw
							),
							reply_markup=inline_HomeworkApprove
						)
					else:
						await query.message.answer_photo(
							photo=hw['photo'],
							caption=await homeworkUploadRewrite(
								date=result['date'],
								subject=data['subject'],
								hw=hw
							),
							reply_markup=inline_HomeworkApprove
						)
						await query.message.delete()
				else:
					if message:
						await message.answer(
							text=await homeworkUploadRewrite(
								date=result['date'],
								subject=data['subject'],
								hw=hw
							),
							reply_markup=inline_HomeworkApprove
						)
					else:
						await query.message.edit_text(
							text=await homeworkUploadRewrite(
								date=result['date'],
								subject=data['subject'],
								hw=hw	
							),
							reply_markup=inline_HomeworkApprove
						)
	except SundayException as exc:
		await message.answer(text=exc.alt)
	except NoLessonAtWeekday as exc:
		await message.answer(text=exc.text)


async def FSM_message_textUpload(message: types.Message, state: FSMContext):
	try:
		subject, task, weekday, date = await ut_handlers.homeworkExtractData(message.from_user.id, message.text)
		await state.set_state(UploadHomeworkFSM.hw_approve)
		await state.set_data({
			'id': message.from_user.id,
			'subject': subject,
			'task': task,
			'weekday': weekday,
			'date': date
		})
		await UploadApprove(
			message=message,
			state=state
		)
		return
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
					'weekday': None,
					'date': None
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
			parse_mode='MarkdownV2'
		)
		exception = 'TimeTravel'
		content = ''
		await state.clear()
	except SundayException as exc:
		await message.answer(text=exc.alt)
		exception = 'SundayException'
		content = ''
	# except Exception as exc:
	# exception = exc
	# content = ''
	await ut_logger.create_log(
		id=message.from_user.id,
		filename=filename,
		function='message_textUpload',
		exception=exception,
		content=content
	)


async def FSM_callback_query_UploadSubmit(query: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	try: data['task']
	except: data['task'] = None
	try: data['photo']
	except: data['photo'] = None
	await operations.setHomework(
		id=query.from_user.id,
		date=data['date'],
		subject=data['subject'],
		task=data['task'],
		photo=data['photo']
	)
	if query.message.caption:
		await query.message.delete()
		await query.message.answer(
			text=await homeworkReUpload(
				date=data['date'],
				subject=data['subject']
			)
		)
	else:
		await query.message.edit_text(
			text=await homeworkReUpload(
				date=data['date'],
				subject=data['subject']
			),
			reply_markup=None
		)
	await state.clear()


async def FSM_callback_query_MistakeCorrect(query: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	if data['message_id'] != query.message.message_id:
		await query.answer()
		return
	# await query.message.edit_text(
		# text=f'Дз на {data["subject"]}',
		# reply_markup=None
	# )
	await state.set_state(UploadHomeworkFSM.hw_approve)
	await UploadApprove(
		query=query,
		state=state
	)


async def FSM_callback_query_Decline(query: types.CallbackQuery, state: FSMContext):
	await query.message.delete()
	await state.clear()


async def FSM_callback_query_DontTouchButtons(query: types.CallbackQuery, state: FSMContext):
	await query.answer()


async def p(message: types.Message):
	print(message.photo[-1])


# <---------- Handlers registration ---------->
def register_handlers(router: Router):
	router.message.register(p, F.photo)
	router.callback_query.register(FSM_callback_query_MistakeCorrect, F.data == 'HomeworkAccept', StateFilter(UploadHomeworkFSM.hw_mistake))
	router.callback_query.register(FSM_callback_query_UploadSubmit, F.data == 'HomeworkAccept', StateFilter(UploadHomeworkFSM.hw_approve))
	router.callback_query.register(FSM_callback_query_Decline, F.data == 'HomeworkDecline', StateFilter(UploadHomeworkFSM))

	router.callback_query.register(FSM_callback_query_DontTouchButtons, F.data.in_({'HomeworkDecline', 'HomeworkAccept'}))

	router.message.register(FSM_message_textUpload, F.text.startswith(ms_regular.hw_keywords))
