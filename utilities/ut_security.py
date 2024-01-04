# <---------- Импорт функций Aiogram ---------->
from aiogram.utils.deep_linking import decode_payload, create_start_link 


# <---------- Импорт локальных функций ---------->
from config import pattern_EncodeDecode


# <---------- Основные функции ---------->
async def ut_EncodeLink(group_id: int, id: int):
	"""
	Encoding unique link for enter group.
	:param group_id: Group ID from database
	:param id: Telegram ID of user who added bot in chat
	:return: link
	"""
	pattern = pattern_EncodeDecode(
		group_id=group_id,
		id=id
	)
	link = await create_start_link(pattern, encode=True)
	return link


async def ut_DecodeLink(argument):
	"""
	Decode unique link to group_id and
	:param argument:
	:return:
	"""
	parameter = decode_payload(argument)
	return parameter
