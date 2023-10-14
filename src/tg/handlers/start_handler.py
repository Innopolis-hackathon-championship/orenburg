from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from api_data.verification import check_verification_code, get_user_by_username
from api_data.register_user import register_user
from keyboards.courier.main_menu_kb import make_main_menu_kb


router = Router()
flags = {"long_operation": "typing"}


class VerifyUser(StatesGroup):
    input_verification_code = State()


@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    user_data, user_exists = await get_user_by_username(message.from_user.username)
    if user_exists:
        if user_data["is_verified"]:
            user_role = user_data["role"]
            if user_role == "courier":
                text = "Вы в главном меню! Ожидайте заказы)"
                reply_markup = await make_main_menu_kb(message.from_user.username)
            else:
                return
        else:
            text = "Добрый день! Для регистрации в системе введите " \
            "код, который вам даст классный руководитель"
            reply_markup = None
    else:
        user_data = {
            "username": message.from_user.username,
            "fullname": message.from_user.first_name,
            "telegram_id": str(message.from_user.id),
            "role": "customer"
        }
        await register_user(user_data)
        text = "Добрый день! Для регистрации в системе введите " \
            "код, который вам даст классный руководитель"
        reply_markup = None
    await message.answer(text=text, reply_markup=reply_markup)
    await state.set_state(VerifyUser.input_verification_code)


@router.message(F.text, VerifyUser.input_verification_code)
async def verify_user(message: Message, state: FSMContext):
    if await check_verification_code(message.from_user.username, message.text):
        await message.answer(
            "Добро пожаловать! Вы в главном меню."
        )
        await state.clear()
    else:
        await message.answer("Код введен неверно. Попробуйте еще раз.")
