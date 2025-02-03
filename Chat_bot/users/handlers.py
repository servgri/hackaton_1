import logging
import json
from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm import context

from core.bot import Form
from users.services import save_user_to_db, user_info_message
# from services import save_user_to_db, user_info_message
from users. utils import fallback_save_to_file, send_final_request
from users.keyboard import create_author_keyboard, create_keyword_keyboard, create_main_keyboard

router = Router()


# Обработчик команды /start
@router.message(CommandStart())
async def send_welcome(message: types.Message, state: context.FSMContext):
    # Извлекаем данные пользователя
    user_info = await user_info_message(message)
    print(user_info)
    
    # Пытаемся сохранить информацию в базу данных
    try:
        await save_user_to_db(user_info)
        logging.info("Пользователь успешно записан в базу данных.")
    except Exception as e:
        # Если не удалось, записываем в файл информацию о пользователе
        logging.error(f"Ошибка сохранения в БД: {str(e)}")
         # Дополнительно, если сохранение в БД провалилось
        await fallback_save_to_file(user_info)

    # Всегда продолжаем работу бота с приветим сообщением
    await message.answer(
        f"Здравствуйте! Я ваш умный гид по Русскому музею.\n"
        f"Какие картины вы бы предпочли сегодня посмотреть?\n"
        f"Введите свой запрос или воспользуйтесь кнопками.",
        reply_markup=create_main_keyboard()
    )
    await state.set_state(Form.phrase)  # Устанавливаем состояние на фразы

# Обработчик состояния "Фраза/запрос"
@router.message(Form.phrase)
async def process_phrase_choice(message: types.Message, state: context.FSMContext):
    user_input = message.text

    if user_input == "Ключевые слова":
        # Переходим к выбору ключевых слов
        await message.answer("Выберите одно или несколько ключевых слов или введите свои:", reply_markup=create_keyword_keyboard())
        await state.set_state(Form.keywords)
    elif user_input == "Автор":
        # Переходим к выбору автора
        await message.answer("Выберите автора из списка или введите имя своего автора:", reply_markup=create_author_keyboard())
        await state.set_state(Form.author)
    else:
        # Пользователь ввел произвольные предпочтения
        await state.update_data(phrase=user_input)  # Сохраняем фразу
        await message.answer("Фраза успешно сохранена! Формирую итоговый запрос...")
        # Используем общую функцию формирования итогового сообщения
        await send_final_request(message, state)


# Обработчик ключевых слов
@router.message(Form.keywords)
async def process_keywords(message: types.Message, state: context.FSMContext):
    user_input = message.text

    if user_input == "Назад":
        await message.answer("Возвращаемся в главное меню.", reply_markup=create_main_keyboard())
        await state.set_state(Form.phrase)
    else:
        # Сохраняем выбранное ключевое слово
        await state.update_data(keywords=user_input)
        await message.answer("Выберите автора из списка или введите имя своего:", reply_markup=create_author_keyboard())
        await state.set_state(Form.author)

# Обработчик авторов
@router.message(Form.author)
async def process_author(message: types.Message, state: context.FSMContext):
    user_author = message.text

    if user_author == "Назад":
        await message.answer("Возвращаемся к выбору фразы или ключевых слов.", reply_markup=create_main_keyboard())
        await state.set_state(Form.phrase)
    else:
        # Сохраняем выбранного автора
        await state.update_data(author=user_author)

        # Используем общую функцию формирования итогового сообщения
        await send_final_request(message, state)