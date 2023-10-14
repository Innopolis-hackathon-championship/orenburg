from aiogram import Router, Bot
from aiogram.types import Message

from api_data.courier.get_orders_queue_data import (
    get_orders_data
)


router = Router()
flags = {"long_operation": "typing"}


async def request_data(bot: Bot):
    data = await get_orders_data()
    if data:
        await bot.send_message(chat_id=944384833, text="Test Text")
    else:
        pass
