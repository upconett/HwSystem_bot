# <---------- Python modules ---------->
from aiogram.utils.deep_linking import decode_payload, create_start_link 


# <---------- Local modules ---------->
from config import pattern_encodeDecode
from create_bot import bot


# <---------- Encode/decode functions ---------->
async def encodeLink(group_id: int, id: int):
	"""
	Encoding unique link for enter group.
	:param group_id: Group ID from database
	:param id: Telegram ID of user who added bot in chat
	:return: link
	"""
	pattern = pattern_encodeDecode(
		group_id=group_id,
		id=id
	)
	link = await create_start_link(
		bot=bot,
		payload=pattern,
		encode=True
	)
	return link


async def decodeLink(argument):
	"""
	Decode unique link to group_id and creator id.
	:param argument: link
	:return:
	"""
	parameter = decode_payload(payload=argument)
	return parameter
