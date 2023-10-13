from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


incoming_order_btns = [
    [InlineKeyboardButton(text="✅ Принять", callback_data="accept")],
    [InlineKeyboardButton(text="❌ Отказаться", callback_data="decline")]
]

incoming_order_keyboard = InlineKeyboardMarkup(
    inline_keyboard=incoming_order_btns
)
