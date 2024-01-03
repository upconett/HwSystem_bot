# <---------- Импорт функций Aiogram ---------->
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup


# <---------- Reply клавиатуры ---------->
btn_reply_MainSchedule_Cancel = KeyboardButton(text='Отмена ❌')
kb_reply_MainSchedule_Cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_reply_MainSchedule_Cancel.add(btn_reply_MainSchedule_Cancel)


# <---------- Inline клавиатуры ---------->
btn_inline_MainSchedule_Submit = InlineKeyboardButton(text='✅', callback_data='MainSchedule_Submit')
btn_inline_MainSchedule_Decline = InlineKeyboardButton(text='❌', callback_data='MainSchedule_Decline')
kb_inline_MainSchedule_Approve = InlineKeyboardMarkup(row_width=2)
kb_inline_MainSchedule_Approve.add(btn_inline_MainSchedule_Submit, btn_inline_MainSchedule_Decline)

btn_inline_MainSchedule_Days1 = InlineKeyboardButton(text='С понедельника по субботу', callback_data='MainSchedule_Days5')
btn_inline_MainSchedule_Days2 = InlineKeyboardButton(text='С понедельника по пятницу', callback_data='MainSchedule_Days4')
kb_inline_MainSchedule_Days = InlineKeyboardMarkup(row_width=1)
kb_inline_MainSchedule_Days.add(btn_inline_MainSchedule_Days1, btn_inline_MainSchedule_Days2)