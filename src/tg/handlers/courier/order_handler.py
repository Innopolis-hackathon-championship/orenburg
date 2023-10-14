from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.courier.validation_kb import (
    in_delivery_keyboard,
    recieve_keyboard
)
from keyboards.courier.rating_kb import rating_keyboard
from keyboards.courier.main_menu_kb import main_menu_keyboard
from filters.pin_filter import PINFilter


router = Router()
flags = {"long_operation": "typing"}


class OrderDelivery(StatesGroup):
    in_delivery = State()
    arrived = State()
    pin_state = State()
    pin_insert = State()
    rate_client = State()


@router.callback_query(Text(startswith="accept_", ignore_case=True))
async def accept_order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    order_id = callback.data.split("_")[1]
    print(order_id)
    await bot.edit_message_text(
        text="Вы приняли заказ #dummy-data...",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=in_delivery_keyboard
    )
    await state.update_data({"order_id": order_id})
    await state.set_state(OrderDelivery.in_delivery)
    await callback.answer()


# TODO: call an api to handle couriers order
@router.callback_query(Text("decline", ignore_case=True))
async def decline_order(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        text="Вы отменили заказ.",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_menu_keyboard
    )
    await callback.answer()


@router.callback_query(
    Text("arrived", ignore_case=True), OrderDelivery.in_delivery
)
async def order_arrived(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    order_id = data["order_id"]
    print(order_id)
    await bot.edit_message_text(
        text='Ожидайте заказчика. По приходу пользователя нажмите на кнопку '
        '"<b>Ввести PIN</b>" для дальнейших инструкций',
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=recieve_keyboard
    )
    await state.set_state(OrderDelivery.pin_state)
    await callback.answer()


@router.callback_query(
    Text("insert_pin", ignore_case=True), OrderDelivery.pin_state
)
async def pin_insert(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(
        text="Введите PIN-код который сказал вам пользователь:",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await state.set_state(OrderDelivery.pin_insert)
    await callback.answer()


@router.message(F.text, OrderDelivery.pin_insert, PINFilter(), flags=flags)
async def successful_order(message: Message, state: FSMContext):
    data = await state.get_data()
    order_id = data["order_id"]
    print(order_id)
    await message.answer(
        "Заказ успешно завершен! Оцените пользователя.",
        reply_markup=rating_keyboard
    )
    await state.set_state(OrderDelivery.rate_client)


@router.message(F.text, OrderDelivery.pin_insert, flags=flags)
async def wrong_pin(message: Message):
    await message.answer("Вы ввели PIN неверно! Попробуйте еще раз")


# TODO: call api to rate client
@router.callback_query(
    OrderDelivery.rate_client,
    Text(startswith="rate_", ignore_case=True)
)
async def rating_client(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = callback.data.split("_")[1]
    if int(data) > 0:
        data = await state.get_data()
        order_id = data["order_id"]
        text = "Спасибо, ваш голос учтен! Ожидайте следующего заказа или уходите с линии."
    else:
        text = "Ожидайте следующего заказа или уходите с линии."
    await bot.edit_message_text(
        text=text,
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_menu_keyboard
    )
    await state.clear()
    await callback.answer()
