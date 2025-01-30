from aiogram import types, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm import context
from core.bot import Form
from users.users_info import user_info_message

router = Router()


# Обработчик команды /start
@router.message(CommandStart())
async def send_welcome(message: types.Message, state: context.FSMContext):
    user_info_message(message)
    await message.answer(f"Здравствуйте! Я ваш умный гид по Русскому музею.\n"
                         f"Какие картины вы бы предпочли сегодня посмотреть?")
    await state.set_state(Form.phrase)  # Устанавливаем состояние на фразы

# Обработчик фразы
@router.message(Form.phrase)
async def process_phrase(message: types.Message, state: context.FSMContext):
    await state.update_data(phrase=message.text)  # Сохраняем фразу
    await message.answer(f"Какой автор вас интересует?")
    await state.set_state(Form.author)   # Переходим к следующему состоянию

# Обработчик автора
@router.message(Form.author)
async def process_author(message: types.Message, state: context.FSMContext):
    user_author = message.text
    if not user_author:
        await message.answer("Пожалуйста, введите корректного автора.")
        return
    await state.update_data(author=user_author)  # Сохраняем автора
    data = await state.get_data()  # Получаем все данные
    await message.answer(f"Ваш запрос:\n"
                         f"Ваши предпочтения: {data['phrase']}\n"
                         f"Автор: {data['author']}.\nСпасибо за выбор!")
    await state.clear()  # Очищаем состояние после завершения

    # Формируем данные для API
    preferences = {
        "phrase": data['phrase'],
        "author": data['author']
    }


    print(preferences)

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
