# <---------- Импорт функций Pyrogram ---------->
from pyrogram import Client


# <---------- Импорт локальных функций ---------->
import create_bot
api_id = create_bot.api_id
api_hash = create_bot.api_hash
MAIN_TOKEN = create_bot.MAIN_TOKEN

# <---------- Основные функции ---------->
async def ut_GetChatMembers(chat_id: int):
	"""
	Opens new connection with Telegram Client API for getting chat members.
	:param chat_id: Telegram chat ID
	:return: List with member`s ids
	"""
	try:
		app = Client("dev_session", api_id=api_id, api_hash=api_hash, bot_token=MAIN_TOKEN, in_memory=True)
		chat_members = []
		await app.start()
		async for member in app.get_chat_members(chat_id):
			chat_members = chat_members + [member.user.id]
		await app.stop()
		return chat_members
	except Exception as exception:
		print(exception)
