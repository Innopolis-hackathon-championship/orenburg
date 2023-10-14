from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.filters.text import Text

from api_data.courier.change_user_state import change_user_state
from keyboards.courier.main_menu_kb import make_main_menu_kb

router = Router()


@router.callback_query(Text(startswith="make_", ignore_case=True))
async def courier_status_change(callback: CallbackQuery, bot: Bot):
    state = callback.data.split("_")[1]
    await change_user_state(
        callback.from_user.username,
        False if state == "online" else True
    )
    await bot.edit_message_text(
        text="Вы в главном меню!",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=await make_main_menu_kb(callback.from_user.username)
    )
