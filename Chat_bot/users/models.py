from typing import  List
from sqlalchemy import String, Boolean, BigInteger, NullPool, func, DateTime, JSON, ForeignKey, Enum as SAEnum, Integer
from sqlalchemy.orm import  mapped_column, Mapped
from datetime import datetime, timezone
from enum import Enum as PyEnum

from core.db import Base


# Определение ролей
class UserRole(PyEnum):
   MODERATOR = "MODERATOR"
   USER = "USER"
   ADMIN = "ADMIN"
   BLOCKED = "BLOCKED"



class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True,primary_key=True, nullable=False)  # Уникальный Telegram ID

    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    username:  Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), nullable=False)
    preferences: Mapped[List] = mapped_column(JSON, nullable=True)
    language_code: Mapped[str | None] = mapped_column(String, nullable=True)
    
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


    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name} ({self.username})"
