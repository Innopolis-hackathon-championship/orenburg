from aiogram.filters import BaseFilter
from aiogram.types import Message


# TODO: add pin validation (mb do this using backend)
class PINFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text == "1234":
            return True
        return False