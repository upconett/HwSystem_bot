# <---------- Python modules ---------->
from aiogram import Router


# <---------- Local modules ---------->
from utilities.ut_filters import *


# <---------- Base router ---------->
router_base = Router()


# <---------- Private routers ---------->
#     <- Router for private chat ->
router_private = Router()
router_private.message.filter(ChatType(['private']))

#     <- Router for private chat and group admin ->
router_private_groupAdmin = Router()
router_private_groupAdmin.message.filter(ChatType(['private']), UserIsGroupAdmin(flag=True))

#     <- Router for private chat and group admin, chat admin if bot is admin ->
router_private_complex = Router()
router_private_complex.message(
	ChatType(chat_types=['group', 'supergroup']),
	UserIsChatAdmin(flag=True),
	UserPresenceInGroup(flag=True),
	BotIsAdministrator(flag=True)
)


# <---------- Group/supergroup routers ---------->
#     <- Router for private chat ->
router_chat = Router()
router_chat.message.filter(ChatType(['group', 'supergroup']))


# <---------- Reg/unreg routers ---------->
#     <- Router for registered users ->
router_registered = Router()
router_registered.message.filter(UserRegister(flag=True))

#     <- Router for unregistered users ->
router_unregistered = Router()
router_unregistered.message.filter(UserRegister(flag=False))
