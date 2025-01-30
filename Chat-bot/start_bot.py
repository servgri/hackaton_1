import sys
import os
import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm import context


from handlers import register_handlers

# Добавить родительскую директорию в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import api_settings


# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Создаем экземпляры бота и диспетчера
bot = Bot(token=api_settings.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация обработчиков
register_handlers(dp)


# # Обработчик всех других текстовых сообщений
# @dp.message(F.text)
# async def echo_message(message: types.Message):
#     await message.answer(f"Вы сказали: {message.text}")

# Функция для старта бота (асинхронная)
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
       try:
           asyncio.run(main())
       except Exception as e:
           logging.error(f"Ошибка при запуске бота: {str(e)}")