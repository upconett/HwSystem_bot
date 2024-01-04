# <---------- Импорт функций Aiogram ---------->
from aiogram.filters import Filter
from aiogram.types import Message


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
