from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()


class ApiSettings(BaseSettings):
    API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # Игнорируем лишние переменные


class DatabaseSettings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # Игнорируем лишние переменные


try:
    api_settings = ApiSettings()
    db_settings = DatabaseSettings()
except Exception as e:
    print(f"Ошибка загрузки конфигурации: {e}")
    exit(1)