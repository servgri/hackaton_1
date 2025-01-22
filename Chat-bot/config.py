from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_TOKEN: str
    # DB_USERNAME: str
    # DB_PASSWORD: str
    # DB_HOST: str
    # DB_PORT: int
    # DB_NAME: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except Exception as e:
    print(f"Ошибка загрузки конфигурации: {e}")
    exit(1)