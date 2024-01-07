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
	'Отлично, теперь давайте пароль!'
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
		f'Отлично, группа создана ✅\n'
		f'Название группы: *{group_name}*\n'
		f'Установлен пароль: *||{group_password}||*'
	)
