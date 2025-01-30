import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import MetaData

from core.config import settings

DATABASE_URL = settings.DATABASE_URL

class Base(DeclarativeBase):
    pass

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логов SQL
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



if __name__ == "__main__":
    asyncio.run(init_db())

