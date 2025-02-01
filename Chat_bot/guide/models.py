from datetime import date
from sqlalchemy import String, LargeBinary, Date, Integer, func, DateTime, BigInteger
from sqlalchemy.orm import  mapped_column, Mapped
from datetime import datetime, timezone

# from Chat_bot.core.db import Base
from core.db import Base

class Image(Base):
    __tablename__ = "images"

    catalog_num: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    items: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    typology: Mapped[str] = mapped_column(String, nullable=False)
    author_lastname: Mapped[str] = mapped_column(String, nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)
    author_patronymic: Mapped[str] = mapped_column(String, nullable=False)
    date_category: Mapped[str] = mapped_column(String, nullable=False)
    cluster: Mapped[int] = mapped_column(Integer, nullable=True)
    key_words: Mapped[str] = mapped_column(String, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
                                 DateTime(timezone=True), 
                                default=lambda: datetime.now(timezone.utc), 
                                server_default=func.now()
                                )
    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), 
    default=lambda: datetime.now(timezone.utc), 
    server_default=func.now(), 
    onupdate=func.now()
)







