# <---------- Импорт функций Aiogram ---------->
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup


# <---------- Reply клавиатуры ---------->
btn_reply_MainSchedule_Cancel = KeyboardButton(text='Отмена ❌')
kb_reply_MainSchedule_Cancel = ReplyKeyboardMarkup(
	keyboard=[[btn_reply_MainSchedule_Cancel]],
	resize_keyboard=True
)


# <---------- Inline клавиатуры ---------->
btn_inline_MainSchedule_Submit = InlineKeyboardButton(text='✅', callback_data='MainSchedule_Submit')
btn_inline_MainSchedule_Decline = InlineKeyboardButton(text='❌', callback_data='MainSchedule_Decline')
kb_inline_MainSchedule_Approve = InlineKeyboardMarkup(
	inline_keyboard=[[btn_inline_MainSchedule_Submit, btn_inline_MainSchedule_Decline]]
)

btn_inline_MainSchedule_Days5 = InlineKeyboardButton(text='С понедельника по субботу', callback_data='MainSchedule_Days5')
btn_inline_MainSchedule_Days4 = InlineKeyboardButton(text='С понедельника по пятницу', callback_data='MainSchedule_Days4')
kb_inline_MainSchedule_Days = InlineKeyboardMarkup(
	inline_keyboard=[
		[btn_inline_MainSchedule_Days5],
		[btn_inline_MainSchedule_Days4]
		]
)