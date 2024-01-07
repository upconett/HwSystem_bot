# <---------- Python modules ---------->
from aiogram import Router


# <---------- Local modules ---------->
from utilities.ut_filters import *


# <---------- Base router ---------->
router_base = Router()


# <---------- Private routers ---------->
#     <- Router for private chat ->
router_private = Router()
router_private.message.filter(ChatType(chat_types=['private'], data_type='message'))

#     <- Router for private chat and group admin ->
router_private_groupAdmin = Router()
router_private_groupAdmin.message.filter(ChatType(chat_types=['private'], data_type='message'), UserIsGroupAdmin())


# <---------- Group/supergroup routers ---------->
#     <- Router for private chat ->
router_chat = Router()
router_chat.my_chat_member.filter(ChatType(chat_types=['group', 'supergroup'], data_type='message'))

#     <- Router for private chat and group admin, chat admin if bot is admin ->
router_chat_complex = Router()
router_chat_complex.callback_query.filter(
	ChatType(chat_types=['group', 'supergroup'], data_type='callback_query'),
	BotIsAdministrator(data_type='callback_query'),
	UserIsChatAdmin(data_type='callback_query'),
	UserPresenceInGroup()
)


# <---------- Reg/unreg routers ---------->
#     <- Router for registered users ->
router_registered = Router()
router_registered.message.filter(UserRegister())

#     <- Router for unregistered users ->
router_unregistered = Router()
router_unregistered.message.filter(~UserRegister())
