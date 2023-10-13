from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
flags = {"long_operation": "typing"}


# TODO: api request to validate couriers
@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        'Здравствуйте! Я - <b>Бот Школьной Столовой</b>! '
        'Я помогу вам узнать статус вашего заказа) Чтобы начать, '
        'нажмите на кнопку <b>"Открыть приложение"</b>'
    )
