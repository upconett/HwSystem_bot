# <---------- Импорт функций Aiogram ---------->
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# <---------- Inline клавиатуры ---------->
async def kb_inline_ConnectGroup(group_ids: list, group_names: list):
	button = InlineKeyboardButton(text='👥 Привязать группу', callback_data=f'ConnectGroup|{group_ids}|{group_names}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.row(button)
	return reply_markup


async def kb_inline_SelectGroup(groups: list):
	reply_markup = InlineKeyboardMarkup(row_width=2)
	group_ids = groups[0]
	group_names = groups[1]
	for i in range(len(group_ids)):
		button = InlineKeyboardButton(text=group_names[i], callback_data=f'ChosenGroup|{group_ids[i]}|{group_names[i]}')
		reply_markup.row(button)
	return reply_markup


async def kb_inline_ChatSettings(group_id: int, group_name: str):
	button0 = InlineKeyboardButton(text='🔔 Включить', callback_data=f'ChatSettings|{group_id}|{group_name}|True')
	button1 = InlineKeyboardButton(text='🔕 Выключить', callback_data=f'ChatSettings|{group_id}|{group_name}|False')
	reply_markup = InlineKeyboardMarkup(row_width=2)
	reply_markup.row(button0, button1)
	return reply_markup


async def kb_inline_GroupLink(group_id: int, group_name: str, link: str):
	button0 = InlineKeyboardButton(text=f'📲 Вступить в {group_name}', url=link)
	button1 = InlineKeyboardButton(text='🧨 Удалить ссылку', callback_data=f'DeleteLink|{group_id}|{group_name}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.row(button0).row(button1)
	return reply_markup


btn_inline_TryAgain = InlineKeyboardButton(text='🔄 Попробовать снова', callback_data=f'ReloadChat')
kb_inline_ReloadChat = InlineKeyboardMarkup(row_width=1)
kb_inline_ReloadChat.row(btn_inline_TryAgain)


async def kb_inline_BoundChatStart(group_id: int, group_name: str):
	button0 = InlineKeyboardButton(text=f'Отвязать {group_name}', callback_data=f'UnlinkGroup|{group_id}|{group_name}')
	button1 = InlineKeyboardButton(text=f'Продолжить', callback_data=f'ContinueWithGroup|{group_id}|{group_name}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.row(button0).row(button1)
