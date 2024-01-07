# <---------- Python modules ---------->
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


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
    def __init__(self, chat_types: list[str], data_type: str) -> None:
        """

        :param chat_types: Group, Supergroup, Channel or Private
        :param data_type: message, callback_query
        """
        self.chat_types = chat_types
        self.data_type = data_type

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if chat type correct
        """
        # print('a', self.data_type, data.chat.type)
        if self.data_type == 'message':
            if data.chat.type in self.chat_types:
                return True
            return False
        elif self.data_type == 'callback_query':
            if data.message.chat.type in self.chat_types:
                return True
            return False
        return False


class BotIsAdministrator(Filter):
    """
    Check if bot chat administrator.
    """
    def __init__(self, flag: bool, data_type: str) -> None:
        """

        :param flag: True (check if bot is admin) or False (check if bot is not admin)
        :param data_type: message, callback_query
        """
        self.flag = flag
        self.data_type = data_type

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if chat type correct
        """
        # print('b')
        if self.data_type == 'message':
            return (await data.from_user.bot.get_me()).can_read_all_group_messages == self.flag
        elif self.data_type == 'callback_query':
            return (await data.message.from_user.bot.get_me()).can_read_all_group_messages == self.flag
        return False


class TextEquals(Filter):
    """
    Checks if message.text matches one of the elements of the given list.
    """
    def __init__(self, list_ms: list[str], data_type: str) -> None:
        """

        :param list_ms: List of messages
        :param data_type: message, callback_query
        """
        self.list_ms = list_ms
        self.data_type = data_type

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if message.text in given list
        """
        # print('c')
        if self.data_type == 'message':
            if data.text.lower() in self.list_ms:
                return True
            return False
        elif self.data_type == 'callback_query':
            if data.data.lower() in self.list_ms:
                return True
            return False
        return False


class UserRegister(Filter):
    """
    Checks the presence of a user in a group or vice versa.
    """
    def __init__(self, flag: bool = True) -> None:
        """

        :param flag: True (check if user in group) or False (check if user not in group)
        """
        self.flag = flag

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        # print('d')
        try:
            response = await operations.userData(id=data.from_user.id)
            result = response['username'] is not None
            return self.flag == result
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserRegister"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserPresenceInGroup(Filter):
    """
    Checks the presence of a user in a group or vice versa.
    """
    def __init__(self, flag: bool = True) -> None:
        """

        :param flag: True (check if user in group) or False (check if user not in group)
        """
        self.flag = flag

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        # print('e')
        try:
            response = await operations.userData(id=data.from_user.id)
            result = response['group_id'] is not None
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

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        # print('f')
        try:
            response = await operations.userData(id=data.from_user.id)
            return self.flag == response['group_admin']
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsGroupAdmin"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserIsGroupOwner(Filter):
    """
    Check if user is group owner or vice versa.
    """
    def __init__(self, flag: bool) -> None:
        self.flag = flag

    async def __call__(self, data: Message) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        # print('g')
        try:
            response = (await psql.select(
                table='groups',
                what='group_id',
                where='owner_id',
                where_value=data.from_user.id
            ))[0][0]
            return response == self.flag
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsGroupOwner"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserIsChatAdmin(Filter):
    """
    Check if user is chat admin with a lot of rights (not like a role) or vice versa.
    """
    def __init__(self, flag: bool, data_type: str) -> None:
        """

        :param flag: True (check if user is chat admin) or False (check if user is not chat admin)
        :param data_type: message, callback_query
        """
        self.flag = flag
        self.data_type = data_type

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        # print('h')
        try:
            if self.data_type == 'message':
                chat_admins = await data.chat.get_administrators()
            elif self.data_type == 'callback_query':
                chat_admins = await data.message.chat.get_administrators()
            else:
                return False
            for user in range(len(chat_admins)):
                if (data.from_user.id == chat_admins[user].user.id) == self.flag:
                    if chat_admins[user].status == 'creator':
                        return True
                    elif chat_admins[user].can_delete_messages and chat_admins[user].can_restrict_members:
                        return True
            return False
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsChatAdmin"; CONTENT=""; EXCEPTION="{exception}";')
            return False
