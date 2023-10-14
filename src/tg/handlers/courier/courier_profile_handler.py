from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters.text import Text

from api_data.courier.get_courier_data import get_courier_data
from keyboards.courier.profile_kb import profile_keyboard
from keyboards.courier.main_menu_kb import make_main_menu_kb


router = Router()


@router.callback_query(Text("profile"))
async def profile_view(callback: CallbackQuery, bot: Bot):
    courier_data = await get_courier_data(callback.from_user.username)
    profile_text = f"<b>Имя</b>: {courier_data['fullname']}\n" \
        f"<b>Рейтинг</b>: {courier_data['rating']}"
    await bot.edit_message_text(
        text="<b>Ваш профиль</b>:\n" + profile_text,
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=profile_keyboard
    )
    await callback.answer()


@router.callback_query(Text("back_to_menu", ignore_case=True))
async def back_to_menu(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        text="Вы в главном меню :)",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=await make_main_menu_kb(callback.from_user.username)
        )
    await callback.answer()
