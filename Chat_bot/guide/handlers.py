from aiogram import Router, types

router = Router()


# Обработка upload_painting
@router.callback_query(lambda callback_query: callback_query.data == "upload_painting")
async def handle_upload_painting(callback_query: types.CallbackQuery):
    await callback_query.answer("You clicked 'Upload a Painting'!")
