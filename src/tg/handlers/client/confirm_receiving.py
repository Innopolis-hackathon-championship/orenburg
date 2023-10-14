from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.filters.text import Text

from api_data.client.confirm_recieving import confirm


router = Router()


@router.callback_query(Text(startswith="comfirm:", ignore_case=True))
async def confirming(callback: CallbackQuery, bot: Bot):
    order_id = callback.data.split(":")[1]
    await confirm(order_id)
    await bot.edit_message_text(
        text="Получение подтверждено!",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await callback.answer()
