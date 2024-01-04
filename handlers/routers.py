# <---------- Импорт функций Aiogram ---------->
from aiogram import Router


# <---------- Импорт локальных функций ---------->
from utilities.ut_filters import *


# <---------- Описание Роутеров ---------->
router_private_member = Router()
router_private_member.message(filter_UserIsAdmin(False))

router_private_admin = Router()
router_private_admin.message(filter_UserIsAdmin())

router_private = Router()
router_private.message(filter_ChatType(['private']))
router_private.include_routers(
	router_private_member,
	router_private_admin
)


router_group_member = Router()
router_group_member.message(filter_UserIsAdmin(False))

router_group_admin = Router()
router_group_admin.message(filter_UserIsAdmin())

router_group = Router()
router_group.message(filter_ChatType(['group', 'supergroup']))
router_group.include_routers(
	router_group_member,
	router_group_admin
)


router_registered = Router()
router_registered.message(filter_UserInGroup())
router_registered.include_routers(
	router_private,
	router_group
)

router_unregistered = Router()
router_unregistered.message(filter_UserInGroup(False))
