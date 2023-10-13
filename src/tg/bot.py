import os
import asyncio

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import start_handler
from handlers.courier import (
    order_handler,
    courier_profile_handler,
    send_order_handler
)
from middlewares.chat_action import ChatActionMiddleware


# TODO: make an env variable
async def main():
    bot = Bot(
        token="5805274347:AAHocXLBPPKM21iJDmtgCEMApTNcQEbrzkE",
        parse_mode="HTML"
    )
    dp = Dispatcher()

    dp.message.middleware(ChatActionMiddleware())

    dp.include_routers(
        start_handler.router,
        order_handler.router,
        courier_profile_handler.router
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_order_handler.request_data, 
        args=[bot], 
        trigger="interval", 
        seconds=5
    )
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
