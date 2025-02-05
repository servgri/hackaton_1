import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData
from datetime import date
from sqlalchemy import String, LargeBinary, Date, Integer, func, DateTime, BigInteger
from sqlalchemy.orm import  mapped_column, Mapped
from datetime import datetime, timezone

# from Chat_bot.core.config import settings
from core.config import settings

DATABASE_URL = settings.DATABASE_URL


# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логов SQL
# Создаем фабрику сессий для взаимодействия с базой данных (транзакции)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False,
                             expire_on_commit=False)


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
   

# if __name__ == "__main__":
#     asyncio.run(init_db())

