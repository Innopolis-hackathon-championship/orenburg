from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from api_data.courier.get_courier_data import get_courier_data


async def make_main_menu_kb(username: str) -> InlineKeyboardMarkup:
    courier_data = await get_courier_data(username)
    is_online = courier_data["is_online"]
    main_menu_btns = [
        [
            InlineKeyboardButton(
                text="✅ На линию", callback_data="make_online")
        ]
        if not is_online else
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
    return InlineKeyboardMarkup(inline_keyboard=main_menu_btns)
