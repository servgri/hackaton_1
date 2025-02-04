import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.db import  async_session_maker 
from users.models import User
from aiogram.types import User as TelegramUser
from users.schemas import UserInfo


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