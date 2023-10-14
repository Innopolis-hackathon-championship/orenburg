from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.filters.text import Text

from api_data.courier.change_user_state import change_user_state

router = Router()


@router.callback_query(Text(startswith="make_", ignore_case=True))
async def courier_status_change(callback: CallbackQuery, bot: Bot):
    state = callback.data.split("_")[1]
    await change_user_state(
        callback.from_user.username,
        True if state == "online" else False
    )
    await bot.edit_message_text()
