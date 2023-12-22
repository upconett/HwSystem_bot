# <---------- Импорт функций Aiogram ---------->
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# <---------- Импорт сторонних функций ---------->
from json import loads


# <---------- Inline клавиатуры ---------->
async def kb_inline_ConnectGroup(group_ids: list, group_names: list):
	button = InlineKeyboardButton(text='👥 Привязать группу', callback_data=f'ConnectGroup|{group_ids}|{group_names}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.row(button)
	return reply_markup


async def kb_inline_SelectGroup(groups: list):
	reply_markup = InlineKeyboardMarkup(row_width=2)
	group_ids = loads(groups[0])
	group_names = loads(groups[1])
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
	button1 = InlineKeyboardButton(text='🧨 Удалить ссылку', callback_data=f'DeleteLink|{group_id}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.row(button0, button1)
	return reply_markup


async def kb_inline_ReloadChat(message):
	button0 = InlineKeyboardButton(text='▶️ Попробовать снова', callback_data=f'ReloadChat|{message}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.row(button0)
	return reply_markup
