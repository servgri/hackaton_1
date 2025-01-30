from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict

from models import UserRole


 # Pydantic модель для валидации
class SUserModel(BaseModel):
    id: int | None  # Поле id будет необязательным (обычно задаётся автоматически в БД)
    telegram_id: int
    first_name: str | None  # Поле full_name необязательное
    last_name: str | None
    username: str | None
    is_active: bool = True
    is_bot: bool = False
    role: UserRole  # Указываем тип Enum для роли
    preferences: List[str] | None # preferences - это список строк или None
    language_code: str | None
    created_at: date
    updated_at: date

    model_config = ConfigDict(from_attributes=True)  # Включаем поддержку ORM-моделей для преобразования из SQLAlchemy объектов