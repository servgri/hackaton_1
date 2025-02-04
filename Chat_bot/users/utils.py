import logging
import json


async def fallback_save_to_file(user_info: dict):
    """
    Резервное сохранение информации о пользователе в файл.
    """
    try:
        with open("backup_users.json", "a", encoding="utf-8") as f:
            json.dump(user_info, f, ensure_ascii=False)
            f.write("\n")
        logging.info("Данные пользователя записаны в резервный файл.")
    except Exception as e:
        logging.error(f"Не удалось записать данные пользователя в файл: {e}")

