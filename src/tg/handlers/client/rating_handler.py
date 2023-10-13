from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.filters.text import Text


router = Router()


# TODO: call api to save rating
@router.callback_query(Text(startswith="rate:", ignore_case=True))
async def rate_order(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        text="Ваш отзыв будет учтен! Спасибо!",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await callback.answer()
