1. Установка виртуального окружения

```
# Создание виртуального окружения для проекта
python -m venv venv

# Активировать виртуальное окружение Для Windoms
venv\Scripts\activate

# Активировать виртуальное окружение Для Linux
source venv/bin/activate

# Отключить виртуальное окружение
deactivate
```

2. Установка зависимостей
```
pip install -r requirements.txt
```

3.  Миграции

```
# Создается папка migrations и файл alembic.ini. В терминале:
alembic init migrations
# Генерация миграции
alembic revision --autogenerate -m "Create users table"
# Применение миграции
alembic upgrade head
# Откатить миграцию
alembic downgrade -1
```