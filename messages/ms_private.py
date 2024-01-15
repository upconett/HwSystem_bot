# <---------- Python modules ---------->
from datetime import datetime


# <---------- Local modules ---------->
from messages import ms_regular


# <---------- Simple messages ---------->
#            <- commands.py ->
commandStartOrHelp_forGroupMember = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Основные функции:\n'
	' · Актуальные домашние задания\n'
	'   /hw\n'
	' · Актуальное расписание\n'
	'   /schedule\n'
	' · Предстоящие события\n'
	'   /events\n'
	' · Панель управления группой\n'
	'   /group'
)


commandStartOrHelp_forNotGroupMember = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Самое время войти в группу или создать её 👇'
)


groupPanel_forNotMember = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Хотите войти в группу или создать её?'
)


groupPanel_forMember = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Хотите выйти из группы?'
)


groupPanel_forOwner = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Вы можете удалить группу, либо передать права управления ею.'
)


#         <- group_create.py ->
groupRegisterName = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Введите название вашей будущей группы 👇'
)


groupRegisterPassword = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Чудное название, теперь давайте придумаем пароль!'
)


groupRegisterPassword_set = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Пароль задан!'
)


#         <- group_enter.py ->
groupEnterName = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Название группы, в которую хотите войти 👇'
)


groupEnterName_noGroup = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Группы с таким названием нет 🧐\n'
	'Попробуйте ещё раз 👇'
)


groupEnterPassword = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Отлично, теперь введите пароль от данной группы!'
)


groupEnterPassword_incorrect = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Пароль неверный!'
)

groupEnterPassword_correct = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Пароль верный!'
)


#     <- default_schedule_upload.py ->
scheduleSet = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Изменение основного расписания ✏️'
)


studyDays = 'В какие дни вы учитесь? ✍️'


studyDays_from0to4 = 'Вы выбрали расписание с понедельника по пятницу.'


studyDays_from0to5 = 'Вы выбрали расписание с понедельника по субботу.'


scheduleLoad = '<b>Установить основное раписание?</b>'


scheduleUpdate = '<b>Обновить основное расписание?</b>'


scheduleLoaded = 'Основное расписание установлено!'


scheduleLoadDecline = 'Обновление основного расписания отменено ⭕'


scheduleElseUpload = (
	'Вы не можете использовать другие функции!\n'
	'Сначала <b>завершите обновление расписания!</b>'
)


scheduleUpdateFinish = 'Обновление расписания завершено...'


# <---------- Complex messages ---------->
#            <- commands.py ->
async def commandStartOrHelp_forNotRegistered(first_name: str):
	return (
		f'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
		f'Привет, <b>{first_name}</b> 👋\n'
		f'Я помогу упорядочить твои знания\n'
		f'Начни со вступления в группу или её создания прямо сейчас 👇'
	)


#     <- default_schedule_upload.py ->
async def currentDaySchedule_accusativeCase(current_day: str):
	return f'Введите расписание на {current_day} 👇'


async def scheduleApprove(len_subjects: int):
	return (
		f'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
		f'<b>Подтверждение расписания</b> 📋\n'
		f'<b>В расписании {len_subjects} предметов:</b>\n'
	)


async def scheduleAppearance(schedule: str):
	return f'\n\n<b>Расписание будет записано так:</b>\n\n{schedule}'


#         <- group_create.py ->
async def groupRegisterFinish(group_name: str, group_password: str):
	return (
		f'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
		f'Отлично, группа создана ✅\n'
		f'Название группы: *{group_name}*\n'
		f'Установлен пароль: *||{group_password}||*'
	)


#         <- group_enter.py ->
async def groupEnterFinish(group_name: str):
	return (
		f'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
		f'Теперь вы состоите в группе: <b>{group_name}</b>'
	)


noMainSchedule = (
	'В вашей группе не установлено <b>основное расписание</b> 📋\n'
	'Попросите <b>админов вашей группы</b> установить его 🛠️'
)


def homeworkShow(date: datetime, tasks: dict, schedule: dict) -> str:
	month = ms_regular.months_genitive[date.month-1]
	weekday = ms_regular.weekdays[date.weekday()]
	result = (
		'<b>📝 Домашнее задание</b>\n'
		f'<b>{weekday.capitalize()} ({date.day} {month} {date.year})</b>\n\n'
	)
	if not tasks:
		result += 'Сохранённых заданий нет 🕊️'
		return result
	sc_subj = set(schedule.values())
	ls_nums = {}
	for subj in sc_subj:
		ls_nums[subj] = [int(ls) for ls in schedule if schedule[ls] == subj]
	for subj in ls_nums:
		item = ls_nums[subj]
		if len(item) == 1:
			ls_nums[subj] = str(item[0])
		elif item == list(range(min(item), max(item)+1)):
			ls_nums[subj] = str(min(item)) + "-" + str(max(item))
		else:
			ls_nums[subj] = ", ".join([str(i) for i in item])
	least = False
	for lesson in tasks:
		if tasks[lesson]['task'] or tasks[lesson]['photos']:
			least = True
			result +=f'<b>[{ls_nums[lesson]}] {lesson.capitalize()}</b>'
			if tasks[lesson]['photos']:
				result += ' 🖼️'
			result += '\n'
			if tasks[lesson]['task']:
				for record in tasks[lesson]['task'].split('\n\n'):
					result += f' • <em>{record}</em>\n'
			result += '\n'
	if not least:
		result += 'Сохранённых заданий нет 🕊️'
	return result

