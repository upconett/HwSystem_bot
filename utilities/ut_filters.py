# <---------- Python modules ---------->
from aiogram.filters import Filter
from aiogram.types import Message


# <---------- Local modules ---------->
from data_base import operations
from create_bot import psql


# <---------- Variables ---------->
filename = 'ut_filters.py'


# <---------- Filter classes ---------->
class ChatType(Filter):
    """
    Check if chat type from message in given chat types list.
    """
    def __init__(self, chat_types: list[str]) -> None:
        """

        :param chat_types: Group, Supergroup, Channel or Private
        """
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        """

        :param message: Aiogram message object
        :return: True if chat type correct
        """
        if message.chat.type in self.chat_types:
            return True
        else:
            return True


class BotIsAdministrator(Filter):
    """
    Check if chat type from message in given chat types list.
    """
    def __init__(self, flag: bool) -> None:
        """

        :param flag:
        """
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        """

        :param message: Aiogram message object
        :return: True if chat type correct
        """
        return (await message.from_user.bot.get_me()).can_read_all_group_messages == self.flag


class TextEquals(Filter):
    """
    Checks if message.text matches one of the elements of the given list.
    """
    def __init__(self, list_ms: list[str]) -> None:
        """

        :param list_ms: List of messages
        """
        self.list_ms = list_ms

    async def __call__(self, message: Message) -> bool:
        """

        :param message: Aiogram message object
        :return: True if message.text in given list
        """
        if message.text:
            if message.text.lower() in self.list_ms:
                return True


class UserRegister(Filter):
    """
    Checks the presence of a user in a group or vice versa.
    """
    def __init__(self, flag: bool) -> None:
        """

        :param flag: True (check if user in group) or False (check if user not in group)
        """
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        """

        :param message: Aiogram message object
        :return: True if the specified condition is met
        """
        try:
            data = await operations.userData(id=message.from_user.id)
            result = data['username'] is not None
            return self.flag == result
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserRegister"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserPresenceInGroup(Filter):
    """
    Checks the presence of a user in a group or vice versa.
    """
    def __init__(self, flag: bool) -> None:
        """

        :param flag: True (check if user in group) or False (check if user not in group)
        """
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        """

        :param message: Aiogram message object
        :return: True if the specified condition is met
        """
        try:
            data = await operations.userData(id=message.from_user.id)
            result = data['group_id'] is not None
            return self.flag == result
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserPresenceInGroup"; CONTENT=""; EXCEPTION="{exception}";')
            return False
    

class UserIsGroupAdmin(Filter):
    """
    Check if user is group admin or vice versa.
    """
    def __init__(self, flag: bool) -> None:
        """

        :param flag: True (check if user in group) or False (check if user not in group)
        """
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        """

        :param message: Aiogram message object
        :return: True if the specified condition is met
        """
        try:
            data = await operations.userData(id=message.from_user.id)
            return self.flag == data['group_admin']
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsGroupAdmin"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserIsGroupOwner(Filter):
    """
    Check if user is group owner or vice versa.
    """
    def __init__(self, flag: bool) -> None:
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        try:
            response = (await psql.select(
                table='groups',
                what='group_id',
                where='owner_id',
                where_value=message.from_user.id
            ))[0][0]
            return response == self.flag
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsGroupOwner"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserIsChatAdmin(Filter):
    """
    Check if user is chat admin with a lot of rights (not like a role) or vice versa.
    """
    def __init__(self, flag: bool) -> None:
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        try:
            chat_admins = await message.chat.get_administrators()
            await message.answer(str(chat_admins), parse_mode=None)
            for user in range(len(chat_admins)):
                if (message.from_user.id == chat_admins[user].user.id) == self.flag:
                    if chat_admins[user].status == 'creator':
                        return True
                    elif chat_admins[user].can_delete_messages and chat_admins[user].can_restrict_members:
                        return True
            return False
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsChatAdmin"; CONTENT=""; EXCEPTION="{exception}";')
            return False
