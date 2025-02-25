import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from Chat_bot.core.bot import dp, bot
from Chat_bot.users.handlers import router as users_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Функция, которая настроит командное меню (дефолтное для всех пользователей)
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт")
        
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault)


# Функция запуска бота
async def on_startup(dispatcher: Dispatcher):
    await set_commands(dispatcher.bot)


# Асинхронный запуск диспетчера
async def main():
    # Подключаем роутеры
    dp.include_router(users_router)

    # Запускаем polling
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == '__main__':
       try:
           asyncio.run(main())
       except Exception as e:
           logging.error(f"Ошибка при запуске бота: {str(e)}")
