import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, select, text
import sys
import os

# Добавить родительскую директорию в sys.path
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DATABASE_URL


async def reflect_schema():
    async_engine = create_async_engine(DATABASE_URL)
    metadata = MetaData()

    async with async_engine.connect() as conn:
        # Reflect the schema into the metadata object
        await conn.run_sync(metadata.reflect)
    
    # Print reflected table names
    print(metadata.tables.keys())


asyncio.run(reflect_schema())


# #Сырой запрос
# # Создайте асинхронный движок подключения
# engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логов SQL

# # Создайте асинхронную сессию
# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )

# # Глобальная метадата для работы с таблицами через рефлексию
# metadata = MetaData()
# async def fetch_data_raw():
#     async with async_session() as session:
#         async with session.begin():
#             # Пример сырого SQL-запроса
#             result = await session.execute(text("SELECT * FROM users"))
            
#             # Печать всех строк
#             for row in result:
#                 print(row)

# asyncio.run(fetch_data_raw())