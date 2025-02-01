from datetime import date
from sqlalchemy import String, LargeBinary, Date, Integer, func, DateTime
from sqlalchemy.orm import  mapped_column, Mapped
from datetime import datetime, timezone

# from Chat_bot.core.db import Base
from core.db import Base

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    title: Mapped[str] = mapped_column(String, nullable=False)
    items: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    typology: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    date_category: Mapped[str] = mapped_column(String, nullable=False)
    key_words: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    catalogue_num: Mapped[int] = mapped_column(Integer, nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)
    author_patrony: Mapped[str] = mapped_column(String, nullable=False)
    cluster: Mapped[int] = mapped_column(Integer, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
                                 DateTime(timezone=True), 
                                default=lambda: datetime.now(timezone.utc), 
                                server_default=func.now()
                                )







