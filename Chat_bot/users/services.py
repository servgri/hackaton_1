import logging
from aiogram import types
from aiogram.fsm import context
from Chat_bot.users.schemas import UserInfo
from Chat_bot.users.keyboard import create_main_keyboard
from Chat_bot.guide.recommendation_system import get_recommendations


async def user_info_message(message) -> UserInfo:
    return UserInfo(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
        is_bot=message.from_user.is_bot,
    )

# Общая функция формирования итогового сообщения
async def send_final_request(message: types.Message, state: context.FSMContext):
    """ 
    Финальная функция для формирования и отправки запроса
    """
    # Получаем данные состояния
    data = await state.get_data()

    # Формируем сообщение
    final_message = (
        f"Ваш запрос собран:\n"
        f"Предпочтения: {data.get('phrase', 'не указаны')}\n"
        f"Ключевые слова: {data.get('keywords', 'не указаны')}\n"
        f"Автор: {data.get('author', 'не указан')}\n"
        f"Спасибо за выбор! Подбираем рекомендации..."
    )

    # Отправляем сообщение пользователю
    await message.answer(final_message, reply_markup=create_main_keyboard())

    # Очищаем состояние
    await state.clear()

    #Формируем строку для поисковика
    preferences = {
        "phrase": data.get('phrase'),
        "author": data.get('author'),
        "keywords": data.get('keywords')
    }

    # Формируем строку запроса для модели
    user_query = f"{data.get('phrase', '')} {data.get('keywords', '')}".strip()
   
   # Проверка: если нет содержимого запроса, отправляем ошибку
    if not user_query:
        await message.answer("Вы не указали предпочтения. Пожалуйста, попробуйте снова.")
        return
    
    # Логируем запрос
    logging.info(f"Итоговый запрос пользователя: {user_query}")
    # return user_query
    # 
    try:
        recommendations = get_recommendations(user_query)

        #  Формируем ответ с рекомендациями
        if recommendations:
            recommendation_text = "\n".join(
                [f"• {item['title']} (Автор: {item['author']}, Категория даты: {item['date_category']})"
                 for item in recommendations]
            )

            # Отправляем рекомендации пользователю
            await message.answer(f"Мы нашли несколько экспонатов для вас:\n{recommendation_text}")
        else:
            # Если экспонатов нет
            await message.answer("К сожалению, мы не нашли подходящих экспонатов для вашего запроса.")
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.answer("Произошла ошибка во время обработки вашего запроса. Попробуйте позже.")


