import requests
import re



def check_image(url: str):
    """Функция для проверки доступности изображения по URL."""
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False


def is_russian_text(text):
    """ Проверка, состоит ли строка только из русских букв"""
    return bool(re.match(r'^[А-Яа-яЁё\s]+$', text))

