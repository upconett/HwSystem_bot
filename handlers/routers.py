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

#     <- Router for private chat and not group member ->
router_private_groupNotMember = Router()
router_private_groupNotMember.message.filter(
	ChatType(chat_types=['private'], data_type='message'),
	~UserPresenceInGroup()
)

#     <- Router for private chat and group member ->
router_private_groupMember = Router()
router_private_groupMember.message.filter(ChatType(chat_types=['private'], data_type='message'), UserPresenceInGroup())
router_private_groupMember.callback_query.filter(
	ChatType(chat_types=['private'], data_type='callback_query'),
	UserPresenceInGroup()
)

#     <- Router for private chat and group admin ->
router_private_groupAdmin = Router()
router_private_groupAdmin.message.filter(ChatType(chat_types=['private'], data_type='message'), UserIsGroupAdmin())
router_private_groupAdmin.callback_query.filter(ChatType(chat_types=['private'], data_type='callback_query'), UserIsGroupAdmin())

#     <- Router for private chat and group owner ->
router_private_groupOwner = Router()
router_private_groupOwner.message.filter(ChatType(chat_types=['private'], data_type='message'), UserIsGroupOwner())
router_private_groupOwner.callback_query.filter(ChatType(chat_types=['private'], data_type='callback_query'), UserIsGroupOwner())

# <---------- Group/supergroup routers ---------->
#     <- Router for group chat ->
router_chat = Router()
router_chat.my_chat_member.filter(ChatType(chat_types=['group', 'supergroup'], data_type='message'))
router_chat.message.filter(ChatType(chat_types=['group', 'supergroup'], data_type='message'))
router_chat.callback_query.filter(ChatType(chat_types=['group', 'supergroup'], data_type='callback_query'))

#     <- Router for group chat and group admin, chat admin if bot is admin ->
router_chat_complex = Router()
router_chat_complex.callback_query.filter(
	ChatType(chat_types=['group', 'supergroup'], data_type='callback_query'),
	BotIsAdministrator(data_type='callback_query'),
	UserIsChatAdmin(data_type='callback_query'),
	UserPresenceInGroup()
)

# <- Router for group chat, registered, groupMember ->
router_chat_groupMember = Router()
router_chat_groupMember.message.filter(UserPresenceInGroup())
router_chat_groupMember.callback_query.filter(UserPresenceInGroup())
router_chat.include_router(router_chat_groupMember)

# <---------- Reg/unreg routers ---------->
#     <- Router for registered users ->
router_registered = Router()
router_registered.message.filter(UserRegister())

#     <- Router for unregistered users ->
router_unregistered = Router()
router_unregistered.message.filter(~UserRegister())
