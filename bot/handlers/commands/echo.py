from aiogram import Router
from bot.config.gettext_config import _
from aiogram.types import Message
from bot.db.crud import use_language_handlers_buttons

echo_router = Router()


@echo_router.message()
async def echo_command(message: Message):
    """
    Handles any unrecognized user message by sending a localized default response.
    This handler is triggered when a user sends a message that does not match any known command.

    """
    tg_id = message.from_user.id
    await use_language_handlers_buttons(tg_id)
    await message.answer(_("echo_message"))