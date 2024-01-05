# <---------- Python modules ---------->
from aiogram import Router


# <---------- Local modules ---------->
from utilities.ut_filters import *


# <---------- Base router ---------->
router_base = Router()


# <---------- Private routers ---------->
#     <- Router for private chat ->
router_private = Router()
router_private.message(ChatType(['private']))

#     <- Router for private chat and group admin ->
router_private_groupAdmin = Router()
router_private_groupAdmin.message(ChatType(['private']), UserIsGroupAdmin(flag=True))


# <---------- Group/supergroup routers ---------->
#     <- Router for private chat ->
router_chat = Router()
router_chat.message(ChatType(['group', 'supergroup']))


# <---------- Reg/unreg routers ---------->
#     <- Router for registered users ->
router_registered = Router()
router_registered.message(UserRegister(flag=True))

#     <- Router for unregistered users ->
router_unregistered = Router()
router_unregistered.message(UserRegister(flag=False))
