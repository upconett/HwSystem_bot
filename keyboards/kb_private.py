# <---------- Python modules ---------->
from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup


# <---------- Variables ---------->
__all__ = [
	'reply_commandStartOrHelp',
	'reply_cancel',
	'inline_groupPanel',
	'inline_groupPanelForNotMember',
	'inline_groupPanelForMember',
	'inline_groupPanelForOwner',
	'inline_mainScheduleApprove',
	'inline_mainScheduleDays',
]


# <---------- Reply keyboards ---------->
#         <- Simple keyboards ->
btn_reply_commandStartOrHelp_0 = KeyboardButton(text='📝 Домашнее задание')
btn_reply_commandStartOrHelp_1 = KeyboardButton(text='📋 Расписание')
btn_reply_commandStartOrHelp_2 = KeyboardButton(text='📌 События')
btn_reply_commandStartOrHelp_3 = KeyboardButton(text='👥 Группа')
btn_reply_commandStartOrHelp_4 = KeyboardButton(text='⚙️ Помощь')
reply_commandStartOrHelp = ReplyKeyboardMarkup(
	keyboard=[
		[btn_reply_commandStartOrHelp_0],
		[btn_reply_commandStartOrHelp_1, btn_reply_commandStartOrHelp_2],
		[btn_reply_commandStartOrHelp_3, btn_reply_commandStartOrHelp_4]
	],
	resize_keyboard=True
)


btn_reply_cancel = KeyboardButton(text='❌ Отмена')
reply_cancel = ReplyKeyboardMarkup(
	keyboard=[[btn_reply_cancel]],
	resize_keyboard=True
)


# <---------- Inline keyboards ---------->
#         <- Simple keyboards ->
btn_inline_groupPanel = InlineKeyboardButton(text='👥 Группа', callback_data='GroupPanel')
inline_groupPanel = InlineKeyboardMarkup(inline_keyboard=[[btn_inline_groupPanel]])


btn_inline_enterGroup = InlineKeyboardButton(text='💼 Войти', callback_data='EnterGroup')
btn_inline_createGroup = InlineKeyboardButton(text='📝 Создать', callback_data='CreateGroup')
inline_groupPanelForNotMember = InlineKeyboardMarkup(inline_keyboard=[[btn_inline_enterGroup, btn_inline_createGroup]])


btn_inline_leaveGroup = InlineKeyboardButton(text='🚪 Выйти', callback_data=f'LeaveGroup')
inline_groupPanelForMember = InlineKeyboardMarkup(inline_keyboard=[[btn_inline_leaveGroup]])


btn_inline_deleteGroup = InlineKeyboardButton(text='🚪 Удалить', callback_data=f'DeleteGroup')
btn_inline_changeOwner = InlineKeyboardButton(text='🔑 Передать права', callback_data=f'ChangeOwner')
inline_groupPanelForOwner = InlineKeyboardMarkup(
	inline_keyboard=[
		[btn_inline_deleteGroup],
		[btn_inline_changeOwner]
	]
)


btn_inline_mainScheduleAccept = InlineKeyboardButton(text='✅', callback_data='MainSchedule_Submit')
btn_inline_mainScheduleDecline = InlineKeyboardButton(text='❌', callback_data='MainSchedule_Decline')
inline_mainScheduleApprove = InlineKeyboardMarkup(inline_keyboard=[[btn_inline_mainScheduleAccept, btn_inline_mainScheduleDecline]])


btn_inline_mainScheduleDays5 = InlineKeyboardButton(text='С понедельника по субботу', callback_data='MainSchedule_Days5')
btn_inline_mainScheduleDays4 = InlineKeyboardButton(text='С понедельника по пятницу', callback_data='MainSchedule_Days4')
inline_mainScheduleDays = InlineKeyboardMarkup(
	inline_keyboard=[
		[btn_inline_mainScheduleDays4],
		[btn_inline_mainScheduleDays5]
	]
)
