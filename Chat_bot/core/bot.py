from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from config import settings


# Создаем экземпляры бота и диспетчера
bot = Bot(token=settings.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определяем состояния для FSM
class Form(StatesGroup):
    menu = State()  # Главное меню
    phrase = State()  # Состояние для ввода фразы
    author = State()  # Состояние для выбора автора
    keywords = State()  # Состояние для выбора ключевых слов
