# <---------- Основные сообщения ---------->
mscl_CommandStartOrHelp_WithGroup = (
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


mscl_CommandStartOrHelp_NoGroup = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Самое время войти в группу или создать её 👇'
)


async def mscl_CommandStartOrHelp_NoRegister(first_name: str):
	return (
		f'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
		f'Привет, <b>{first_name}</b> 👋\n'
		f'Я помогу упорядочить твои знания\n'
		f'Начни со вступления в группу или её создания прямо сейчас 👇'
	)


mscl_GroupPanel_NoGroup = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Хотите войти в группу или создать её?'
)


mscl_GroupPanel_WithGroupNoAdmin = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Хотите выйти из группы?'
)


mscl_GroupPanel_WithGroupAdmin = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Хотите удалить группу?'
)


mscl_RegistergroupStart = (
	'⚙️ <b><a href="https://t.me/HwSystem_bot">HomeWorker_Bot</a></b>\n'
	'Введите название вашей будущей группы\n'
	'Не более 20 символов 👇'
)
