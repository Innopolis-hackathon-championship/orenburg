from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from api_data.verification import check_verification_code
from api_data.register_user import register_user
from keyboards.courier.main_menu_kb import main_menu_keyboard
from keyboards.courier.incoming_order_kb import make_incoming_order_kb


router = Router()
flags = {"long_operation": "typing"}


class VerifyUser(StatesGroup):
    input_verification_code = State()


@router.message(Command("start"), flags=flags)
async def start_cmd(message: Message, state: FSMContext):
    user_data = {
        "username": message.from_user.username,
        "fullname": message.from_user.first_name,
        "telegram_id": message.from_user.id
    }
    await register_user(user_data)
    await message.answer(
        "Добрый день! Для регистрации в системе введите "
        "код, который вам даст классный руководитель"
    )
    await state.set_state(VerifyUser.input_verification_code)


@router.message(F.text, VerifyUser.input_verification_code)
async def verify_user(message: Message, state: FSMContext):
    if await check_verification_code(message.from_user.username, message.text):
        await message.answer(
            "Добро пожаловать! Вы в главном меню.",
            reply_markup=main_menu_keyboard
        )
        await state.clear()
    else:
        await message.answer("Код введен неверно. Попробуйте еще раз.")


# test case of order (will be removed in the future)
@router.message(Command("test"), flags=flags)
async def make_test(message: Message):
    await message.answer("Вам заказ:", reply_markup=make_incoming_order_kb("123"))
