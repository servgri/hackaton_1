import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from core.db import  async_session_maker 
from users.models import User
from aiogram.types import User as TelegramUser
# from models import User
from users.schemas import UserInfo


async def user_info_message(message) -> UserInfo:
    return UserInfo(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
        is_bot=message.from_user.is_bot,
    )

async def save_user_to_db(user_info: UserInfo):
    async with async_session_maker() as session:  # Открываем сессию
        async with session.begin():  # Обособляем операцию в транзакцию
            # Ищем пользователя в базе данных по его telegram_id
            user_in_db = await session.get(User, user_info.telegram_id)
            
            if not user_in_db:  # Если пользователь не найден
                # Создаём запись нового пользователя
                user_in_db = User(**user_info.model_dump())  # Преобразуем Pydantic модель в dict
                session.add(user_in_db)  # Добавляем нового пользователя в сессию
            else:
                # Если пользователь уже существует, обновляем данные полей
                update_data = user_info.model_dump(exclude_unset=True)  
                # exclude_unset: обновляет только те данные, которые явно переданы в модели UserInfo
                for key, value in update_data.items():
                    setattr(user_in_db, key, value)  # Устанавливаем новые значения атрибутов
            
        # Завершаем транзакцию (commit), изменения сохраняются в БД
        await session.commit()

