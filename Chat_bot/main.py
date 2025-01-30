import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from core.bot import dp, bot
from users.handlers import router as users_router
from guide.handlers import router as guide_router


# Функция, которая настроит командное меню (дефолтное для всех пользователей)
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт")
        
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault)



async def on_startup(dispatcher: Dispatcher):
    await set_commands(dispatcher.bot)


async def main():
    # Подключаем роутеры
    dp.include_router(users_router)
    dp.include_router(guide_router)

    # Запускаем polling
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == "__main__":
    asyncio.run(main())
