from datetime import date
from sqlalchemy import String, Date, Integer, func, DateTime, BigInteger
from sqlalchemy.orm import  mapped_column, Mapped
from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector
from Chat_bot.core.db import Base

class Image(Base):
    __tablename__ = "images"
    
    title: Mapped[str]  # nullable=False по умолчанию
    items: Mapped[str] 
    description: Mapped[str] 
    typology: Mapped[str] 
    author: Mapped[str]
    date_category: Mapped[str]
    key_words: Mapped[str]
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)
    cluster: Mapped[int] 
    author_name: Mapped[str]
    author_patronymic: Mapped[str] 
    catalog_num: Mapped[float] 
    registration_date: Mapped[date] 
    image_url: Mapped[str]

    
    
    
    
 






