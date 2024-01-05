# <---------- Python modules ---------->
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# <---------- Inline keyboards ---------->
#          <- Simple keyboards ->
btn_inline_tryAgain = InlineKeyboardButton(text='🔄 Попробовать снова', callback_data='ReloadChat')
inline_reloadChat = InlineKeyboardMarkup(inline_keyboard=[[btn_inline_tryAgain]])


btn_inline_firstMessage = InlineKeyboardButton(text='Начать!', callback_data='StartChat')
inline_firstMessage = InlineKeyboardMarkup(inline_keyboard=[[btn_inline_firstMessage]])


#         <- Complex keyboards ->
async def inline_chatStart(group_ids: list, group_names: list):
	button = InlineKeyboardButton(text='👥 Привязать группу', callback_data=f'Groups|{group_ids}|{group_names}')
	reply_markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
	return reply_markup


async def inline_selectGroup(groups: list):
	group_ids = groups[0]
	group_names = groups[1]
	buttons = []
	for i in range(len(group_ids)):
		button = InlineKeyboardButton(text=group_names[i], callback_data=f'BindGroup|{group_ids[i]}|{group_names[i]}')
		buttons.append([button])
	reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
	return reply_markup


async def inline_bindChatSettings(group_id: int, group_name: str):
	button0 = InlineKeyboardButton(text='🔔 Включить', callback_data=f'ChatSettings|{group_id}|{group_name}|True')
	button1 = InlineKeyboardButton(text='🔕 Выключить', callback_data=f'ChatSettings|{group_id}|{group_name}|False')
	reply_markup = InlineKeyboardMarkup(inline_keyboard=[[button0, button1]])
	return reply_markup


async def inline_boundGroup(group_id: int, group_name: str, link: str):
	button0 = InlineKeyboardButton(text=f'📲 Вступить в {group_name}', url=link)
	button1 = InlineKeyboardButton(text='🧨 Удалить ссылку', callback_data=f'DeleteLink|{group_id}|{group_name}')
	reply_markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[button0],
			[button1]
		]
	)
	return reply_markup


async def inline_chatStart_withBoundGroup(group_id: int, group_name: str):
	button0 = InlineKeyboardButton(text=f'🗑 Отвязать {group_name}', callback_data=f'UnlinkGroup|{group_id}|{group_name}')
	button1 = InlineKeyboardButton(text='🔑 Продолжить', callback_data=f'ContinueWithGroup|{group_id}|{group_name}')
	reply_markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[button0],
			[button1]
		]
	)
	return reply_markup
