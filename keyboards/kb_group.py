# <---------- Импорт функций Aiogram ---------->
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# <---------- Inline клавиатуры ---------->
def kb_inline_ConnectGroup(groups: list):
	button = InlineKeyboardButton(text='👥 Привязать группу', callback_data=f'ConnectGroup {groups}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.add(button)
	return reply_markup

def kb_inline_SelectGroup(groups: list):
	reply_markup = InlineKeyboardMarkup(row_width=2)
	for group_id, group_name in groups:
		button = InlineKeyboardButton(text=group_name, callback_data=f'ChoosedGroup {group_id}')
		reply_markup.row(button)
	return reply_markup
