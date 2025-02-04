from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# # Главная клавиатура
# def create_main_keyboard() -> ReplyKeyboardMarkup:
#     # Структура кнопок — двумерный список
#     keyboard = [
#         [KeyboardButton(text="Фраза"), KeyboardButton(text="Автор"), KeyboardButton(text="Ключевые слова"), KeyboardButton(text="Отправить запрос")]
#     ]
#     return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)

# Главная клавиатура
def create_main_keyboard() -> ReplyKeyboardMarkup:
    # Размещаем все кнопки в одну строку
    keyboard = [
        [KeyboardButton(text="Фраза"), KeyboardButton(text="Автор"), KeyboardButton(text="Ключевые слова")],
        [KeyboardButton(text="Отправить запрос")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)

# # Клавиатура с кнопками "Ключевые слова"
# def create_keyword_keyboard() -> ReplyKeyboardMarkup:
#     keywords = ["Пейзаж", "Портрет", "Бытовой жанр", "Исторический жанр", "Авангард", "Любой"]
#     # Каждое ключевое слово в отдельной строке
#     keyboard = [[KeyboardButton(text=keyword)] for keyword in keywords]
#     # Добавляем кнопку "Назад"
#     keyboard.append([KeyboardButton(text="Назад")])
#     return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

# Клавиатура для выбора "Ключевых слов"
def create_keyword_keyboard() -> ReplyKeyboardMarkup:
    keywords = ["Пейзаж", "Портрет", "Бытовой жанр", "Исторический жанр", "Авангард", "Любой"]
    # Каждое ключевое слово располагаем в отдельной строке
    keyboard = [[KeyboardButton(text=keyword)] for keyword in keywords]
    # Добавляем кнопку "Назад" в новой строке
    keyboard.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

# # Клавиатура с кнопками "Автор"
# def create_author_keyboard() -> ReplyKeyboardMarkup:
#     authors = ["Шишкин", "Айвазовский", "Репин", "Серов", "Врубель", 
#                "Суриков", "Левитан", "Малевич", "Крамской", "Кандинский", "Любой"]
#     # Каждое имя автора в отдельной строке
#     keyboard = [[KeyboardButton(text=author)] for author in authors]
#     # Добавляем кнопку "Назад"
#     keyboard.append([KeyboardButton(text="Назад")])
#     return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

# Клавиатура для выбора "Авторов"
def create_author_keyboard() -> ReplyKeyboardMarkup:
    authors = ["Шишкин", "Айвазовский", "Репин", "Серов", "Врубель", 
               "Суриков", "Левитан", "Малевич", "Крамской", "Кандинский", "Любой"]
    # Каждый автор отображается на отдельной строке
    keyboard = [[KeyboardButton(text=author)] for author in authors]
    # Добавляем кнопку "Назад" в конце
    keyboard.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

# Финальная клавиатура
def create_final_keyboard() -> ReplyKeyboardMarkup:
    # Кнопки "Подтвердить" и "Отмена" в одной строке
    keyboard = [
        [KeyboardButton(text="Подтвердить"), KeyboardButton(text="Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)