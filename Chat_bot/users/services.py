import logging
from aiogram import types
from aiogram.fsm import context
from users.schemas import UserInfo
from users.keyboard import create_main_keyboard
from guide.services import recommend_by_cluster


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

    # Формируем строку запроса для модели
    query = f"{data.get('phrase', '')} {data.get('keywords', '')} {data.get('author', '')}".strip()
   
   # Проверка: если нет содержимого запроса, отправляем ошибку
    if not query:
        await message.answer("Вы не указали предпочтения. Пожалуйста, попробуйте снова.")
        return
    
    # Логируем запрос
    logging.info(f"Итоговый запрос пользователя: {query}")
   
   # Передаём запрос в функциях рекомендаций
    recommendations = recommend_by_cluster(query)

     # Отправляем рекомендации пользователю
    if recommendations is not None and not recommendations.empty:
        recommendation_text = "\n".join(
            [f"• {row['title']} (Кластер: {row['cluster']})" for _, row in recommendations.iterrows()]
        )
        await message.answer(f"Мы нашли несколько экспонатов для вас:\n{recommendation_text}")
    else:
        await message.answer("К сожалению, мы не смогли найти подходящие экспонаты для вашего запроса.")
   


