import os
import asyncio

from aiogram import Bot, Dispatcher

from handlers import (
    start_handler
)
from middlewares.chat_action import ChatActionMiddleware


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# TODO: make an env variable
async def main():
    bot = Bot(token="5805274347:AAHocXLBPPKM21iJDmtgCEMApTNcQEbrzkE", parse_mode="HTML")
    dp = Dispatcher()
    
    dp.message.middleware(ChatActionMiddleware())
    
    dp.include_routers(start_handler.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
