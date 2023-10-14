from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


choice_btns = [
    [InlineKeyboardButton(text="Да, я уверен", callback_data="sure")],
    [InlineKeyboardButton(text="Нет, не стоит", callback_data="not_sure")]
]

choice_keyboard = InlineKeyboardMarkup(inline_keyboard=choice_btns)