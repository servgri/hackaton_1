import logging
import json
from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm import context

from core.bot import Form
from users.services import save_user_to_db, user_info_message
# from services import save_user_to_db, user_info_message
from users. utils import fallback_save_to_file

router = Router()


# Обработчик команды /start
@router.message(CommandStart())
async def send_welcome(message: types.Message, state: context.FSMContext):
    # Извлекаем данные пользователя
    user_info = await user_info_message(message)
    
    # Пытаемся сохранить информацию в базу данных
    try:
        await save_user_to_db(user_info)
        logging.info("Пользователь успешно записан в базу данных.")
    except Exception as e:
        # Если не удалось, записываем в файл информацию о пользователе
        logging.error(f"Ошибка сохранения в БД: {str(e)}")
         # Дополнительно, если сохранение в БД провалилось
        await fallback_save_to_file(user_info)

    # Всегда продолжаем работу бота с приветим сообщением
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


