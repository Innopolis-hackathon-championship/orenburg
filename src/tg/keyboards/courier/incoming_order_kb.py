from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def make_incoming_order_kb(order_id: str) -> InlineKeyboardMarkup:
    incoming_order_btns = [
        [
            InlineKeyboardButton(
                text="✅ Принять", callback_data=f"accept_{order_id}"
            ),
            InlineKeyboardButton(text="❌ Отказаться", callback_data="decline")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=incoming_order_btns)
