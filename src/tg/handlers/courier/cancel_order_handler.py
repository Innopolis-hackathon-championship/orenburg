from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from typing import Optional, Tuple

from keyboards.courier.choice_kb import choice_keyboard
from keyboards.courier.main_menu_kb import main_menu_keyboard

from handlers.courier.order_handler import OrderDelivery
from keyboards.courier.validation_kb import (
    in_delivery_keyboard,
    recieve_keyboard
)


router = Router()
flags = {"long_operation": "typing"}


async def choose_proper_output(state: str) -> \
        Optional[Tuple[str, InlineKeyboardMarkup]]:
    state = state.split(":")[1]
    if state == "in_delivery":
        return (
            "Вы приняли заказ #dummy-data...",
            in_delivery_keyboard
        )
    elif state == "pin_state":
        return (
            'Ожидайте заказчика. По приходу пользователя нажмите на кнопку '
            '"<b>Ввести PIN</b>" для дальнейших инструкций',
            recieve_keyboard
        )
    return None


# TODO: might check about deleting old reply
@router.message(Command("cancel"))
async def cancel_order(message: Message, state: FSMContext):
    state: str = await state.get_state()
    print(state)
    if state != "OrderDelivery:in_delivery" and state != "OrderDelivery:pin_state":
        pass
    else:
        await message.answer(
            "Вы уверены, что хотите отменить доставку заказа? "
            "(При отмене заказа теряется приоритет)",
            reply_markup=choice_keyboard
        )


# TODO: call api
@router.callback_query(Text("sure", ignore_case=True))
async def canceling(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(
        "Вы отменили заказ, ваш рейтинг упал.",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_menu_keyboard
    )
    await state.clear()
    await callback.answer()


@router.callback_query(Text("not_sure", ignore_case=True))
async def do_not_cancel(callback: CallbackQuery, bot: Bot, state: FSMContext):
    state: str = await state.get_state()
    text, reply_markup = await choose_proper_output(state)
    await bot.edit_message_text(
        text=text,
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=reply_markup
    )
    await callback.answer()
