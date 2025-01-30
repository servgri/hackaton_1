import sys
import os
import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData


# Добавить родительскую директорию в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import db_settings

DATABASE_URL = db_settings.DATABASE_URL

class Base(DeclarativeBase):
    pass

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


    async with engine.begin() as connection:
     # необходимо выполнить метаданные для получения информации о таблицах
        metadata = MetaData()
        await connection.run_sync(metadata.reflect)

        # теперь мы можем выводить информацию о таблицах
        print("Таблицы в базе данных:")
        for table in metadata.tables:
            print(table)

if __name__ == "__main__":
    asyncio.run(init_db())