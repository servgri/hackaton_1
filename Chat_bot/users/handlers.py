import logging
from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm import context

from core.bot import Form
from users.dao import save_user_to_db
from users.services import  user_info_message, send_final_request
from users. utils import fallback_save_to_file
from users.keyboard import (
    create_author_keyboard, 
    create_keyword_keyboard, 
    create_main_keyboard, 
    create_final_keyboard,
)

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
        "Какие картины вы бы предпочли сегодня посмотреть?\n"
        "Введите свой запрос или воспользуйтесь кнопками.\n"
        "Когда завершите выбор, нажмите \"Отправить запрос\".",
        reply_markup=create_main_keyboard()
    )
    await state.set_state(Form.menu)  # Устанавливаем начальное состояние


# Обработчик главного меню
@router.message(Form.menu)
async def process_main_menu_choice(message: types.Message, state: context.FSMContext):
    user_input = message.text

    if user_input == "Фраза":
        # Пользователь выбирает фразу
        await message.answer("Введите вашу фразу или текст запроса:")
        await state.set_state(Form.phrase)
    elif user_input == "Ключевые слова":
        # Пользователь переходит к выбору ключевых слов
        await message.answer(
            "Выберите ключевые слова из списка или введите свои:",
            reply_markup=create_keyword_keyboard()
        )
        await state.set_state(Form.keywords)
    elif user_input == "Автор":
        # Пользователь переходит к выбору автора
        await message.answer(
            "Выберите автора из предложенного списка или введите имя:",
            reply_markup=create_author_keyboard()
        )
        await state.set_state(Form.author)
    elif user_input == "Отправить запрос":
        # Пользователь завершает выбор и формирует запрос
        await send_final_request(message, state)
    else:
        # Неверный ввод
        await message.answer(
            "Пожалуйста, выберите одно из предложенных действий или нажмите \"Отправить запрос\".",
            reply_markup=create_main_keyboard()
        )


# Обработчик состояния "Фраза"
@router.message(Form.phrase)
async def process_phrase_choice(message: types.Message, state: context.FSMContext):
    user_input = message.text

    if user_input == "Назад":
        # Переход в главное меню
        await message.answer("Вы вернулись в главное меню.", reply_markup=create_main_keyboard())
        await state.set_state(Form.menu)
    else:
        # Сохраняем фразу в состояние
        await state.update_data(phrase=user_input)
        await message.answer(
            "Фраза успешно сохранена! Вы можете выбрать ключевые слова, автора или нажать \"Отправить запрос\".",
            reply_markup=create_final_keyboard()
        )
        await state.set_state(Form.menu)


# Обработчик состояния "Ключевые слова"
@router.message(Form.keywords)
async def process_keywords(message: types.Message, state: context.FSMContext):
    user_input = message.text

    if user_input == "Назад":
         # Переход в главное меню
        await message.answer("Возвращаемся в главное меню.", reply_markup=create_main_keyboard())
        await state.set_state(Form.menu)
    else:
        # Сохраняем выбранное ключевое слово
        await state.update_data(keywords=user_input)
        await message.answer(
            "Ключевые слова сохранены! Вы можете выбрать фразу, автора или нажать \"Отправить запрос\".",
            reply_markup=create_final_keyboard()
        )
        await state.set_state(Form.menu)

# Обработчик состояния "Автор"
@router.message(Form.author)
async def process_author(message: types.Message, state: context.FSMContext):
    user_author = message.text

    if user_author == "Назад":
        # Переход в главное меню
        await message.answer("Вы вернулись в главное меню.", reply_markup=create_main_keyboard())
        await state.set_state(Form.menu)
    else:
        # Сохраняем автора
        await state.update_data(author=user_author)
        await message.answer(
            "Автор успешно сохранён! Вы можете выбрать фразу, ключевые слова или нажать \"Отправить запрос\".",
            reply_markup=create_final_keyboard()
        )
        await state.set_state(Form.menu)