from aiogram import types, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm import context
from services import Form


# Создаем маршрутизатор
router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def send_welcome(message: types.Message, state: context.FSMContext):
    await message.answer("Здравствуйте! Я ваш умный гид по Русскому музею. Какой стиль картины вас интересует?")
    await state.set_state(Form.style)  # Устанавливаем состояние на стиль

# Обработчик стиля
@router.message(Form.style)
async def process_style(message: types.Message, state: context.FSMContext):
    await state.update_data(style=message.text)  # Сохраняем стиль
    await message.answer(f"Вы выбрали стиль: {message.text}. Какой жанр вас интересует?")
    await state.set_state(Form.genre) # Переходим к следующему состоянию

# Обработчик жанра
@router.message(Form.genre)
async def process_genre(message: types.Message, state: context.FSMContext):
    await state.update_data(genre=message.text)  # Сохраняем жанр
    await message.answer(f"Вы выбрали жанр: {message.text}. Какой период времени вас интересует?")
    await state.set_state(Form.era) # Переходим к следующему состоянию

# Обработчик периода времени
@router.message(Form.era)
async def process_era(message: types.Message, state: context.FSMContext):
    await state.update_data(era=message.text)  # Сохраняем период времени
    await message.answer(f"Вы выбрали период времени: {message.text}. Какой автор вас интересует?")
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
    await message.answer(f"Ваши предпочтения:\n"
                         f"Стиль: {data['style']}\n"
                         f"Жанр: {data['genre']}\n"
                         f"Период: {data['era']}\n"
                         f"Автор: {data['author']}.\nСпасибо за выбор!")
    await state.clear()  # Очищаем состояние после завершения

    # Формируем данные для API
    preferences = {
        "style": data['style'],
        "genre": data['genre'],
        "era": data['era'],
        "author": data['author']
    }


    print(preferences)

# Функция для регистрации обработчиков
def register_handlers(dp: Dispatcher):
    dp.include_router(router)

