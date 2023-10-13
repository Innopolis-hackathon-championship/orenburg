from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters.text import Text

from keyboards.courier.profile_kb import profile_keyboard
from keyboards.courier.main_menu_kb import main_menu_keyboard


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
    await callback.answer()


@router.callback_query(Text("back_to_menu", ignore_case=True))
async def back_to_menu(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        text="Вы в главном меню. Ожидайте заказа или уходите с линии",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_menu_keyboard
        )
    await callback.answer()
