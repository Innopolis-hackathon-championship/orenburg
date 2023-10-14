from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


in_delivery_btns = [
    [InlineKeyboardButton(text="⏱️ Я на месте", callback_data="arrived")],
]


recieve_btns = [
    [InlineKeyboardButton(text="🧑‍💻 Ввести PIN", callback_data="insert_pin")]
]


in_delivery_keyboard = InlineKeyboardMarkup(inline_keyboard=in_delivery_btns)
recieve_keyboard = InlineKeyboardMarkup(inline_keyboard=recieve_btns)
