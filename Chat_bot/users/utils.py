import logging
import json

from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm import context

from core.bot import Form
from users.keyboard import create_main_keyboard


async def fallback_save_to_file(user_info: dict):
    """
    Резервное сохранение информации о пользователе в файл.
    """
    try:
        with open("backup_users.json", "a", encoding="utf-8") as f:
            json.dump(user_info, f, ensure_ascii=False)
            f.write("\n")
        logging.info("Данные пользователя записаны в резервный файл.")
    except Exception as e:
        logging.error(f"Не удалось записать данные пользователя в файл: {e}")


# Вынесенная функция для формирования итогового сообщения
async def send_final_request(message: types.Message, state: context.FSMContext):
    # Получаем данные состояния
    data = await state.get_data()

    # Формируем сообщение
    final_message = (
        f"Ваш запрос собран:\n"
        f"Предпочтения: {data.get('phrase', 'не указаны')}\n"
        f"Ключевые слова: {data.get('keywords', 'не указаны')}\n"
        f"Автор: {data.get('author', 'не указан')}\n"
        f"Спасибо за выбор! Если хотите изменить выбор, нажмите /start."
    )

    # Отправляем сообщение пользователю
    await message.answer(final_message, reply_markup=create_main_keyboard())

    # Очищаем состояние
    await state.clear()

    # Формируем данные для передачи в модель рекомендательной системы
    preferences = {
        "phrase": data.get('phrase'),
        "author": data.get('author'),
        "keywords": data.get('keywords')
    }
    print(preferences)