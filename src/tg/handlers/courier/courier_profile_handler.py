from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters.text import Text

from src.tg.keyboards.courier.profile_kb import profile_keyboard


router = Router()


# TODO: add profile data
@router.callback_query(Text("profile"))
async def profile_view(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        text="<b>Ваш профиль:</b>",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=profile_keyboard
    )
