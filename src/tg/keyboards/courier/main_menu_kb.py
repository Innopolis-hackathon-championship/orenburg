from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# TODO: add check if courier is online or offline
main_menu_btns = [
    [
        InlineKeyboardButton(text="✅ На линию", callback_data="make_online")
    ],
    [
        InlineKeyboardButton(
            text="🛑 Уйти с линии", callback_data="make_offline"
        )
    ],
    [
        InlineKeyboardButton(
            text="👤 Просмотреть профиль", callback_data="profile"
        )
    ]
]

main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=main_menu_btns)
