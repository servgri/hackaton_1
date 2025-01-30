1. Миграции

```
# Создается папка migrations и файл alembic.ini. В терминале:
alembic init migrations
# Генерация миграции
alembic revision --autogenerate -m "Create users table"
# Применение миграции
alembic upgrade head