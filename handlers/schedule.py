# <---------- Импорт функций Aiogram ---------->
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# <---------- Импорт локальных функций ---------->
from create_bot import bot
from data_base.operation import db_psql_UserData, db_psql_InsertUser
from messages.ms_client import *
from messages.ms_regular import *
from keyboards.kb_client import *
from utilities.ut_logger import ut_LogCreate


# <---------- Константы ---------->
states = ['sc_monday', 'sc_tuesday', 'sc_wednesday', 'sc_thursday', 'sc_friday', 'sc_saturday']
days_0 = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
days_1 = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу']


# <---------- Машина состояний ---------->
class UpdateMainScheduleFSM(StatesGroup):
    sc_monday = State()
    sc_tuesday = State()
    sc_wednesday = State()
    sc_thursday = State()
    sc_friday = State()
    sc_saturday = State()


# <---------- Handler функции ---------->
async def schedule_FSM_StartUpload(message: types.Message):
	"""
	Triggered by '/update' - TEST
	:param message:
	:return:
	"""
	try:
		if message.chat.type == 'supergroup' or message.chat.type == 'group':
			await bot.send_message(
				chat_id=message.from_user.id,
				text=f'{message.text} можно использовать только в личных сообщениях!',
				reply_markup=kb_reply_CommandStartOrHelp
				)
			await message.delete()
			content = 'No database operations.'
			exception = 'Used from group.'
		else:
			if await client_IsGroupMember(message.from_id):
				await message.answer(
					'Изменение основного расписания ✏️\n'
					'**Формат:**\n'
					'1 Алгебра\n'
					'2 Биология\n'
					'3 Информатика\n'
					"(Можно '1.' и '1)')", parse_mode='Markdown'
					)
				await message.answer('Введите расписание на Понедельник. 👇')
				await UpdateMainScheduleFSM.sc_monday.set()
			else:
				await message.answer('Вы не состоите в группе. ❌')
	except Exception as exception:
		await ut_LogCreate(
			id=message.from_user.id,
			filename=filename,
			function='client_handler_UpdateMainSchedule',
			exception=exception,
			content=''
		)


async def schedule_FSM_WeekDayInput(message: types.Message, state: FSMContext):
    str_state = await state.get_state()
    str_state = str(str_state).replace('UpdateMainScheduleFSM:', '')
    async with state.proxy() as data:
        data[str_state] = message.text
        if str_state == 'sc_saturday':
            result = ''
            for s in states:
                day = days_0[states.index(s)]
                result += day + "\n" + data[s] + "\n\n"
            await message.answer('Отлично, расписание будет выглядеть так:')
            await message.answer(result)
            await message.answer('Сохранить расписание?')
            await state.finish()
        else:
            day = days_1[states.index(str_state)+1]
            await message.answer(f"Теперь запиши расписание на {day}. 👇")
            await UpdateMainScheduleFSM.next()


def register_handlers_schedule(dp: Dispatcher):
    """
    Регистрация всех message и callback хендлеров для сценария: 'Изменение Основного Расписания'.
    :param dp:
    :return:
    """
    dp.register_message_handler(schedule_FSM_StartUpload, Text(['/update']))
    dp.register_message_handler(schedule_FSM_WeekDayInput, state=[UpdateMainScheduleFSM.sc_monday, UpdateMainScheduleFSM.sc_tuesday, 
                                                                      UpdateMainScheduleFSM.sc_wednesday, UpdateMainScheduleFSM.sc_thursday,
                                                                      UpdateMainScheduleFSM.sc_friday, UpdateMainScheduleFSM.sc_saturday])
