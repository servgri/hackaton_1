from datetime import date
from sqlalchemy import String, Date, Integer, func, DateTime, BigInteger
from sqlalchemy.orm import  mapped_column, Mapped
from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector

# from Chat_bot.core.db import Base
from core.db import Base

class Image(Base):
    __tablename__ = "images_1"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    catalog_num: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    items: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False, index=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    typology: Mapped[str] = mapped_column(String, nullable=False)
    author_lastname: Mapped[str] = mapped_column(String, nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)
    author_patronymic: Mapped[str] = mapped_column(String, nullable=False)
    date_category: Mapped[str] = mapped_column(String, nullable=False)
    cluster: Mapped[int] = mapped_column(Integer, nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)
    key_words: Mapped[str] = mapped_column(String, nullable=False)
    







