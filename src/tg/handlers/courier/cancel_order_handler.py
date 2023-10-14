from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from api_data.courier.cancel_order import cancel_order
from api_data.courier.get_courier_data import get_courier_order
from keyboards.courier.main_menu_kb import make_main_menu_kb


router = Router()
flags = {"long_operation": "typing"}


@router.message(Command("cancel"))
async def cancel_order(message: Message):
    order_id = await get_courier_order(message.from_user.username)
    cancel = await cancel_order(order_id["order_id"])
    if cancel:
        await message.answer(
            text="Вы отменили заказ :( Вы в главном меню.",
            reply_markup=await make_main_menu_kb(message.from_user.username)
        )
    else:
        pass
