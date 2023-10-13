from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.courier.main_menu_kb import main_menu_keyboard
from keyboards.courier.incoming_order_kb import incoming_order_keyboard

router = Router()
flags = {"long_operation": "typing"}


# TODO: api request to validate couriers
@router.message(Command("start"), flags=flags)
async def start_cmd(message: Message):
    await message.answer(
        'Здравствуйте! Я - <b>Бот Школьной Столовой</b>! '
        'Я помогу вам узнать статус вашего заказа) Чтобы начать, '
        'нажмите на кнопку <b>"Открыть приложение"</b>',
        reply_markup=main_menu_keyboard
    )

# test case of order (will be removed in the future)
@router.message(Command("test"), flags=flags)
async def make_test(message: Message):
    await message.answer("Вам заказ:", reply_markup=incoming_order_keyboard)
