# <---------- Python modules ---------->
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


# <---------- Local modules ---------->
from data_base import operations
from create_bot import psql


# <---------- Variables ---------->
filename = 'ut_filters.py'
__all__ = ['ChatType', 'BotIsAdministrator', 'TextEquals', 'UserIsChatAdmin', 'UserRegister', 'UserIsGroupAdmin', 'UserIsGroupOwner', 'UserPresenceInGroup']


# <---------- Filter classes ---------->
class ChatType(BaseFilter):
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
        result = False
        if self.data_type == 'message':
            result = False
            if data.chat.type in self.chat_types:
                result = True
        elif self.data_type == 'callback_query':
            result = False
            if data.message.chat.type in self.chat_types:
                result = True
        print(f'ChatType in {self.chat_types} >> {result}')
        return result


class BotIsAdministrator(BaseFilter):
    """
    Check if bot chat administrator.
    """
    def __init__(self, data_type: str) -> None:
        """

        :param data_type: message, callback_query
        """
        self.data_type = data_type

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if chat type correct
        """
        if self.data_type == 'message':
            chat_admins = await data.chat.get_administrators()
        elif self.data_type == 'callback_query':
            chat_admins = await data.message.chat.get_administrators()
        else:
            print('BotIsAdministrator >> False (incorrect data_type)')
            return False
        result = False
        for user in range(len(chat_admins)):
            if chat_admins[user].status == 'creator':
                continue
            result = False
            if (await data.from_user.bot.get_me()).id == chat_admins[user].user.id:
                result = False
                if chat_admins[user].can_delete_messages and chat_admins[user].can_restrict_members:
                    result = True
                    break
        print(f'BotIsAdministrator >> {result}')
        return result


class TextEquals(BaseFilter):
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
        result = False
        if self.data_type == 'message':
            result = False
            if data.text.lower() in self.list_ms:
                result = True
        elif self.data_type == 'callback_query':
            result = False
            if data.data.lower() in self.list_ms:
                result = True
        print(f'TextEquals to {self.list_ms} >> {result}')
        return result


class UserRegister(BaseFilter):
    """
    Checks the presence of a user in a group or vice versa.
    """

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        try:
            response = await operations.userData(id=data.from_user.id)
            result = response['username'] is not None
            print(f'UserRegister {data.from_user.id} >> {result}')
            return result
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserRegister"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserPresenceInGroup(BaseFilter):
    """
    Checks the presence of a user in a group or vice versa.
    """

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        try:
            response = await operations.userData(id=data.from_user.id)
            result = response['group_id'] is not None
            print(f'UserPresenceInGroup {data.from_user.id} >> {result}')
            return result
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserPresenceInGroup"; CONTENT=""; EXCEPTION="{exception}";')
            return False
    

class UserIsGroupAdmin(BaseFilter):
    """
    Check if user is group admin or vice versa.
    """
    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        try:
            response = await operations.userData(id=data.from_user.id)
            print(f'UserIsGroupAdmin {data.from_user.id} >> {response}')
            return response['group_admin']
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsGroupAdmin"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserIsGroupOwner(BaseFilter):
    """
    Check if user is group owner or vice versa.
    """

    async def __call__(self, data: Message) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        try:
            response = (await psql.select(
                table='groups',
                what='group_id',
                where='owner_id',
                where_value=data.from_user.id
            ))[0][0]
            print(f'UserIsGroupOwner {data.from_user.id} >> {response}')
            return response
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsGroupOwner"; CONTENT=""; EXCEPTION="{exception}";')
            return False


class UserIsChatAdmin(BaseFilter):
    """
    Check if user is chat admin with a lot of rights (not like a role) or vice versa.
    """
    def __init__(self, data_type: str) -> None:
        """

        :param data_type: message, callback_query
        """
        self.data_type = data_type

    async def __call__(self, data: Message or CallbackQuery) -> bool:
        """

        :param data: Aiogram message or callback_query object
        :return: True if the specified condition is met
        """
        try:
            if self.data_type == 'message':
                chat_admins = await data.chat.get_administrators()
            elif self.data_type == 'callback_query':
                chat_admins = await data.message.chat.get_administrators()
            else:
                print('UserIsChatAdmin >> False (incorrect data_type)')
                return False
            result = False
            for user in range(len(chat_admins)):
                result = False
                if data.from_user.id == chat_admins[user].user.id:
                    result = False
                    if chat_admins[user].status == 'creator':
                        result = True
                        break
                    elif chat_admins[user].can_delete_messages and chat_admins[user].can_restrict_members:
                        result = True
                        break
            print(f'UserIsChatAdmin {data.from_user.id} >> {result}')
            return result
        except Exception as exception:
            print(f'FILENAME="{filename}"; CLASS="UserIsChatAdmin"; CONTENT=""; EXCEPTION="{exception}";')
            return False
