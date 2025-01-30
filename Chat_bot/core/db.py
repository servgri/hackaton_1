import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData

from Chat_bot.core.config import settings
#from config import settings

DATABASE_URL = settings.DATABASE_URL


# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логов SQL
# Создаем фабрику сессий для взаимодействия с базой данных (транзакции)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# if __name__ == "__main__":
#     asyncio.run(init_db())

