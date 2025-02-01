from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главная клавиатура
def create_main_keyboard() -> ReplyKeyboardMarkup:
    # Структура кнопок — двумерный список
    keyboard = [
        [KeyboardButton(text="Ключевые слова"), KeyboardButton(text="Автор")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)

# Клавиатура с кнопками "Ключевые слова"
def create_keyword_keyboard() -> ReplyKeyboardMarkup:
    keywords = ["Пейзаж", "Портрет", "Бытовой жанр", "Исторический жанр", "Авангард", "Любой"]
    # Каждое ключевое слово в отдельной строке
    keyboard = [[KeyboardButton(text=keyword)] for keyword in keywords]
    # Добавляем кнопку "Назад"
    keyboard.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

# Клавиатура с кнопками "Автор"
def create_author_keyboard() -> ReplyKeyboardMarkup:
    authors = ["Шишкин", "Айвазовский", "Репин", "Серов", "Врубель", 
               "Суриков", "Левитан", "Малевич", "Крамской", "Кандинский", "Любой"]
    # Каждое имя автора в отдельной строке
    keyboard = [[KeyboardButton(text=author)] for author in authors]
    # Добавляем кнопку "Назад"
    keyboard.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)



