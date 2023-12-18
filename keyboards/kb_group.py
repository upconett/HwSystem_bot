# <---------- Импорт функций Aiogram ---------->
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# <---------- Inline клавиатуры ---------->
def kb_inline_connectGroup(groups: list):
	button = InlineKeyboardButton(text='👥 Привязать группу ', callback_data=f'ConnectGroup {groups}')
	reply_markup = InlineKeyboardMarkup(row_width=1)
	reply_markup.add(button)
	return reply_markup
