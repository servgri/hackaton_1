import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем параметры подключения
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

# Создаем движок для подключения к базе данных
DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(DATABASE_URL)

def check_image_urls(table_name, output_file='unavailable_urls.txt', batch_size=1000):
    offset = 0
    while True:
        # Получаем следующий пакет URL из базы данных
        query = f'SELECT image_url FROM {table_name} LIMIT {batch_size} OFFSET {offset};'
        df = pd.read_sql(query, engine)

        # Проверяем, получили ли мы какие-либо данные
        if df.empty:
            break  # Если данных больше нет, выходим из цикла

        # Список недоступных URL
        unavailable_urls = []

        # Проверяем доступность каждого URL
        for url in df['image_url']:
            try:
                response = requests.head(url, allow_redirects=True)
                # Если ответ некорректен (например, 404 или 403), добавляем в список
                if response.status_code != 200:
                    unavailable_urls.append(url)
            except requests.exceptions.RequestException:
                # В случае ошибки добавляем URL в список
                unavailable_urls.append(url)

        # Записываем недоступные URL в файл
        if unavailable_urls:
            with open(output_file, 'a') as f:  # Используем 'a' для добавления в конец файла
                for url in unavailable_urls:
                    f.write(url + '\n')

        # Увеличиваем смещение
        offset += batch_size

# Запускаем функцию
check_image_urls('backup_images')

