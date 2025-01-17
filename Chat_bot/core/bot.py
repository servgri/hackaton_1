from aiogram import Bot, Dispatcher, Router
from Chat_bot.core.config import settings

bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher()
