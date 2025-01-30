from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

from Chat_bot.core.config import settings


# Создаем экземпляры бота и диспетчера
bot = Bot(token=settings.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определяем состояния для FSM
class Form(StatesGroup):
    phrase = State()
    author = State()

