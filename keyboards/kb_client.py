# <---------- Импорт функций Aiogram ---------->
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup


# <---------- Reply клавиатуры ---------->
btn_reply_CommandStartOrHelp_0 = KeyboardButton(text='📝 Домашнее задание')
btn_reply_CommandStartOrHelp_1 = KeyboardButton(text='📋 Расписание')
btn_reply_CommandStartOrHelp_2 = KeyboardButton(text='📌 События')
btn_reply_CommandStartOrHelp_3 = KeyboardButton(text='👥 Группа')
btn_reply_CommandStartOrHelp_4 = KeyboardButton(text='⚙️ Помощь')
kb_reply_CommandStartOrHelp = ReplyKeyboardMarkup(resize_keyboard=True)
kb_reply_CommandStartOrHelp.add(btn_reply_CommandStartOrHelp_0)
kb_reply_CommandStartOrHelp.row(btn_reply_CommandStartOrHelp_1, btn_reply_CommandStartOrHelp_2)
kb_reply_CommandStartOrHelp.row(btn_reply_CommandStartOrHelp_3, btn_reply_CommandStartOrHelp_4)


# <---------- Inline клавиатуры ---------->
btn_inline_GroupPanel = InlineKeyboardButton(text='👥 Группа', callback_data='GroupPanel')
kb_inline_GroupPanel = InlineKeyboardMarkup(row_width=1)
kb_inline_GroupPanel.add(btn_inline_GroupPanel)


btn_inline_Help = InlineKeyboardButton(text='⚙️ Помощь', callback_data='ButtonHelp')
kb_inline_Help = InlineKeyboardMarkup(row_width=1)
kb_inline_Help.add(btn_inline_Help)
