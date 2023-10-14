from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api_data.courier.order_confirmation import decline_order, confirm_order
from api_data.courier.change_order_state import (
    change_order_state,
    delivery_arrived
)
from api_data.courier.get_courier_data import get_courier_order
from keyboards.courier.validation_kb import (
    in_delivery_keyboard,
    recieve_keyboard
)
from keyboards.courier.rating_kb import rating_keyboard
from keyboards.courier.main_menu_kb import make_main_menu_kb
from filters.pin_filter import PINFilter


router = Router()
flags = {"long_operation": "typing"}


class OrderDelivery(StatesGroup):
    in_delivery = State()
    arrived = State()
    pin_state = State()
    pin_insert = State()
    rate_client = State()


# TODO: call api to handle orders
@router.callback_query(Text(startswith="courier_offer:", ignore_case=True))
async def accept_order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    order_id, status = callback.data.split(":")[1], callback.data.split(":")[2]
    if status == "decline":
        await decline_order(order_id)
        await bot.edit_message_text(
            text="Вы отменили заказ.",
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=await make_main_menu_kb(callback.from_user.username)
        )
    else:
        address, code = await confirm_order(order_id, callback.from_user.id)
        await bot.edit_message_text(
            text=f"Вы приняли заказ.\n<b>Доставка в</b>: {address}\n"
            f"<b>Код для получения</b>: {code}",
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=in_delivery_keyboard
        )
        await state.set_state(OrderDelivery.in_delivery)
    await callback.answer()


@router.callback_query(
    Text("arrived", ignore_case=True), OrderDelivery.in_delivery
)
async def order_arrived(callback: CallbackQuery, bot: Bot, state: FSMContext):
    order_id = get_courier_order(callback.from_user.username)
    order_id = order_id["order_id"]
    await delivery_arrived(str(order_id))
    await bot.edit_message_text(
        text='Ожидайте заказчика. По приходу он подтвердит заказ.',
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await state.set_state(OrderDelivery.pin_state)
    await callback.answer()


# # TODO: call api to rate client
# @router.callback_query(
#     OrderDelivery.rate_client,
#     Text(startswith="rate_", ignore_case=True)
# )
# async def rating_client(callback: CallbackQuery, bot: Bot, state: FSMContext):
#     data = callback.data.split("_")[1]
#     if int(data) > 0:
#         order_id = get_courier_order(callback.from_user.username)
#         order_id = order_id["order_id"]
#         text = "Спасибо, ваш голос учтен! Ожидайте следующего заказа или уходите с линии."
#     else:
#         text = "Ожидайте следующего заказа или уходите с линии."
#     await bot.edit_message_text(
#         text=text,
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         reply_markup=await make_main_menu_kb(callback.from_user.username)
#     )
#     await state.clear()
#     await callback.answer()
