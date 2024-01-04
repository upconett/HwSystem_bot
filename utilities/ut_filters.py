# <---------- Импорт функций Aiogram ---------->
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


# <---------- Импорт локальных функций ---------->
from data_base.operation import *


# <---------- Основные классы ---------->
class filter_ChatType(Filter):
    """
    Check chat type.
    """
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        for chat_type in self.chat_types:
            if message.chat.type == chat_type:
                return True


class filter_UserInGroup(Filter):
    """
    Check if user has group.
    """
    def __init__(self, flag:bool=True) -> None:
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        user_data = await db_psql_UserData(message.from_user.id)
        return self.flag == user_data['group_id']