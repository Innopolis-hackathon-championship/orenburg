from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


profile_btns = [
    [
        InlineKeyboardButton(
            text="⏪ Обратно в меню", callback_data="back_to_menu"
        )
    ]
]

profile_keyboard = InlineKeyboardMarkup(inline_keyboard=profile_btns)
