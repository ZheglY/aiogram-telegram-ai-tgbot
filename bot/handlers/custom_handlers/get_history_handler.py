from aiogram.types import CallbackQuery
from aiogram import Router
from bot.db.crud import get_user_history_by_id

get_history_router = Router()


@get_history_router.callback_query(lambda c: c.data.startswith("history_id_"))
async def get_history_handler(callback_query: CallbackQuery):
    """
    Handle a button that leads to a specific history record in the database

    - Extracts the history ID from the callback data.
    - Fetches the corresponding record from the database.
    - Sends the retrieved message or data back to the user.
    """
    await callback_query.answer()
    history_id = callback_query.data[11:]
    response_text = await get_user_history_by_id(history_id)
    await callback_query.message.answer(response_text)
