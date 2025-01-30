from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User


async def create_user(session: AsyncSession, username: str):
    user = User(username=username)
    session.add(user)
    await session.commit()

# Сохраняем данные пользователя в словарь user_data
def user_info_message(message):
    user_data = {}  # Используется как пример. Лучше использовать базу данных для реальных ботов.
    # Создаем переменную для хранения данных пользователей
    user = message.from_user  # Получаем объект User (пользователь)
    
    # Сохраняем данные пользователя в словарь user_data
    user_info = {
        "telegram_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
        "is_bot": user.is_bot
    }
    user_data[user.id] = user_info  # Сохраняем данные под Telegram ID
    
    print(user_data)