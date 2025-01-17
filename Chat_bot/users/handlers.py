from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Добро пожаловать! Я бот.")

#
# @router.message(Command("start"))
# async def send_welcome(message: Message):
#     user_id = message.from_user.id
#     user = get_user(user_id)
#     if not user:
#         add_user(user_id=user_id,
#                  username=message.from_user.username,
#                  first_name=message.from_user.first_name,
#                  last_name=message.from_user.last_name,
#                  role_id=0)
#         user = get_user(user_id=user_id)
#     username = user.get('username')
#     role_id = user.get('role_id')
#
#     if role_id == 1:
#         await message.answer(f"Добро пожаловать, {username}!\nВы зашли как {role_id}.", reply_markup=admin_keyboard)
#     elif role_id == 2:
#         await message.answer(f"Добро пожаловать, {username}!\nВы зашли как {role_id}.", reply_markup=moderator_keyboard)
#     elif role_id == 0:
#         await message.answer(f"Добро пожаловать, {username}!", reply_markup=inline_user_keyboard)
#     else:
#         await message.answer("Доступ запрещен!")
