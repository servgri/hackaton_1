import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData

#from Chat_bot.core.config import settings
from core.config import settings

DATABASE_URL = settings.DATABASE_URL


# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логов SQL
# Создаем фабрику сессий для взаимодействия с базой данных (транзакции)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False,
                             expire_on_commit=False)



# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# if __name__ == "__main__":
#     asyncio.run(init_db())

