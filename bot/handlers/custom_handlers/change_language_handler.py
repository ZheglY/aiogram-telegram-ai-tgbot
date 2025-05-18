from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.db.crud import new_language_handlers_buttons
from bot.config.gettext_config import _
import logging
from bot.keyboard.inline.inline_buttons import menu_button


logger = logging.getLogger("bot_logger")

change_language_router = Router()


@change_language_router.callback_query(lambda c: c.data.startswith("lang_user_"))
async def change_user_language(callback_query: CallbackQuery, state:FSMContext):
    """
    Handler for the bot localization

    - The function gets the user id and language specified in the tg profile.
    It updates the user's language in the database and sets the new language as the bot interface.
    After that it immediately takes the user to the bot menu
    """
    await callback_query.answer()
    tg_id = callback_query.from_user.id
    language = callback_query.data[-2:]
    await new_language_handlers_buttons(tg_id=tg_id,language=language)
    await callback_query.message.answer(text=_("menu_message"), reply_markup=menu_button(language=language))
