import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start_handler
from handlers.courier import (
    order_handler,
    courier_profile_handler,
    cancel_order_handler,
    state_handler
)
from handlers.client import confirm_receiving, rating_handler
from middlewares.chat_action import ChatActionMiddleware


# TODO: make an env variable
async def main():
    bot = Bot(
        token="5805274347:AAHocXLBPPKM21iJDmtgCEMApTNcQEbrzkE",
        parse_mode="HTML"
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(ChatActionMiddleware())

    dp.include_routers(
        start_handler.router,
        order_handler.router,
        courier_profile_handler.router,
        cancel_order_handler.router,
        state_handler.router,
        confirm_receiving.router,
        rating_handler.router
    )


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
