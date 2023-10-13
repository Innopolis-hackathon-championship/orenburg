from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# rate:order_num:rating
rating_btns = [
    [
        InlineKeyboardButton(
            text=f"{i}", callback_data=f"rate_{i}"
        ) for i in range(1, 6)
    ],
    [InlineKeyboardButton(text="Нет, спасибо", callback_data="rate_0")]
]


rating_keyboard = InlineKeyboardMarkup(inline_keyboard=rating_btns)
