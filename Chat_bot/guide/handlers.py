from aiogram import Router, types
# from guide.services import recommend_by_cluster, kmeans_model, data

router = Router()


# # Обработчик текста пользователя
# @router.message_handler()
# async def handle_message(message: types.Message):
#     user_query = message.text
#     recommended_items = recommend_by_cluster(user_query, data, kmeans_model)

#     if recommended_items:
#         await message.reply(f"Рекомендованные картины: {recommended_items}") 

# # Тут что-то добавим типа вызова картины и описания из бд
#     else:
#         await message.reply("Извините, я не смог найти подходящих картин по вашему запросу.")

# # Или предложим просто какой-то набор картин..

# Обработка upload_painting
@router.callback_query(lambda callback_query: callback_query.data == "upload_painting")
async def handle_upload_painting(callback_query: types.CallbackQuery):
    await callback_query.answer("You clicked 'Upload a Painting'!")