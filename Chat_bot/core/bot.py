from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

from core.config import settings
# from config import settings


# Создаем экземпляры бота и диспетчера
bot = Bot(token=settings.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определяем состояния для FSM
class Form(StatesGroup):
    phrase = State()  # Состояние для фразы
    author = State()  # Состояние при выборе Автора
    keywords = State()  # Состояние при выборе Ключевых слов

