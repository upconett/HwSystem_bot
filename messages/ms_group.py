# <---------- Python modules ---------->
from datetime import datetime


# <---------- Local modules ---------->
from messages.ms_regular import months_genitive, weekdays 


#<---------- Simple messages ---------->
chatFirstMessage = 'Прошу права администратора, а затем нажать на кнопочку 👇'


chatFirstMessageEdited = 'Настройка начата.'


chatStart = (
	'Привет, ученики 👋\n'
	'Спасибо, что добавили меня в этот чат!\n'
	'Для работы мне нужны <b>права администратора</b>\n'
	'И чтобы ваша группа была супергруппой, для этого она не должна быть частной 🔓\n'
	'Как выдадите, нажмите сюда 👇'
)


chatStart_notSupergroup = (
	'Ваш чат не является супергруппой!\n'
	'Сделайте его общедоступным по ссылке, а не частным 🔓\n'
	'После этого перепригласите бота в чат'
)


chatStart_noGroups = (
	'Участники данного чата не состоят ни в одной группе 😕\n'
	'Чтобы я смог работать, пускай хоть один из них создаст или вступит в группу\n'
	'Затем вы сможете нажать эту кнопку 👇'
)


newBotInChat = 'О, у меня появился друг? Спасибо ❤️‍'


selectGroup = (
	'Отлично 🤓\n'
	'В вашем чате я вижу участников данных групп, выберите к какой из них привязать бота 👇'
)


bindChatSettings = 'Теперь выберите, хотите ли вы получать уведомления о предстоящих уроках, приближающихся звонках и скорых событиях?'


chatReloaded = 'Ваш чат <b>успешно</b> перезагружен!'


chatReloadError = (
	'<b>Ошибка</b> перезапуска!\n'
	'Лучше уж удалите меня из чата.. 🥺'
)


# <---------- Complex messages ---------->
async def chatStart_withBoundGroup(group_name: str):
	return (
		f'Кажется, этот чат уже привязан к группе <b>{group_name}</b>\n'
		f'Хотите её отвязать или продолжим работать с ней?'
	)


async def boundGroup_withLink(group_name: str):
	return (
		f'Отлично, ваш чат привязан к группе <b>{group_name}</b> 🔗\n'
		f'Под этим сообщением я оставляю <b>ссылку</b> на быстрое вступление в вашу группу без пароля (для учатников чата, кто ещё не присоединился)\n'
		f'Будьте бдительны, ведь переход по ней позволит злоумышленникам начать творить хаос среди вашей домашки 👹\n'
		f'На случай опаски, вторая кнопка удаляет кнопку со ссылкой и деактивирует её 😃'
	)


async def boundGroup_withoutLink(group_name: str, full_name: str, username: str):
	return (
		f'Отлично, ваш чат привязан к группе <b>{group_name}</b> 🔗\n'
		f'Ссылка для быстрого вступления была удалена админом <a href="https://t.me/{username}">{full_name}</a> 😃'
	)


async def unlinkGroup(group_name: str):
	return f'Этот чат был отвязан от группы <b>{group_name}</b> 🔓'


def homeworkUpload(date: datetime, subject:str):
	month = months_genitive[date.month-1]
	weekday = weekdays[date.weekday()]
	result = (
		f'<b>Задание сохранено ✅</b>\n'
		f'{weekday.capitalize()} ({date.day} {month} {date.year})'
	)
	return result


def homeworkReUpload(date: datetime, subject:str):
	month = months_genitive[date.month-1]
	weekday = weekdays[date.weekday()]
	result = (
		f'<b>Задание перезаписано ✅</b>\n'
		f'{weekday.capitalize()} ({date.day} {month} {date.year})'
	)
	return result


def homeworkUploadAdd(date: datetime, subject:str):
	month = months_genitive[date.month-1]
	weekday = weekdays[date.weekday()]
	result = (
		f'<b>Задание дополнено ✅</b>\n'
		f'{weekday.capitalize()} ({date.day} {month} {date.year})'
	)
	return result


def homeworkUploadRewrite(date: datetime, subject:str, hw: dict):
	month = months_genitive[date.month-1]
	weekday = weekdays[date.weekday()]
	task = hw['task']
	if task is None:
		task = 'Фото ☝️'
	result = (
		f'<b>{subject.capitalize()}</b>\n'
		f'{weekday.capitalize()} ({date.day} {month} {date.year})\n'
		f'Похоже задание на этот урок уже было записано:\n\n'
		f'<em>{task}</em>\n\n'
		'✏️ <b>Добавить</b>\n'
		'🆕 <b>Перезаписать</b>\n'
		'❌ <b>Отменить</b> '
	)
	return result


separateMessage = (
	'✏️ <b>Добавить</b>\n'
	'🆕 <b>Перезаписать</b>\n'
	'❌ <b>Отменить</b> '
)