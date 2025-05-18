import logging

from aiogram.fsm.context import FSMContext

from bot.config.gettext_config import _

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.keyboard.inline.inline_buttons import menu_button, support_button, history_buttons
from bot.states.all_states import MenuState

from bot.db.crud import check_user_set_language, use_language_handlers_buttons, get_user_history

from bot_init import bot


logger = logging.getLogger("bot_logger")
basic_commands_router = Router()


@basic_commands_router.message(CommandStart())
async def start(message: Message):
    """
    Handler for the /start command.

    - Registers the user if they are not already registered and sends a localized  welcome message.
    - If the user is already registered, sends a localized welcome-back message with menu buttons.
    - Button in the handler offers 2 options. 1 - generate text 2 - generate image
    """

    tg_id = message.from_user.id
    language = message.from_user.language_code
    if not await check_user_set_language(tg_id=tg_id, language=language):
        await message.answer(_("welcome_message"), reply_markup=menu_button(language=language))
    else:
        user_language = await use_language_handlers_buttons(tg_id)
        await message.reply(_("already_registered_welcome_message"), reply_markup=menu_button(language=user_language))



@basic_commands_router.message(Command("help"))
async def help_command(message: Message):
    """
    Handler for /help command.

    - Handler shows all bot commands, allows the user to change the language of the bot interface
    and allows to send feedback on possible bugs
    - sets the interface language for the buttons (use_language_handlers_buttons)
    """
    tg_id = message.from_user.id
    user_language = await use_language_handlers_buttons(tg_id) # sets the interface language for the buttons
    await message.reply(_("help_message"), reply_markup=support_button(user_language))



@basic_commands_router.message(MenuState.menu)
@basic_commands_router.message(Command("menu"))
async def menu_command(message: Message, state: FSMContext):
    """
    Handler for /menu command.

    - Clears current state.
    - Sends menu text with localized buttons.
    - sets the interface language for the buttons (use_language_handlers_buttons)
    - Button in the handler offers 2 options. 1 - generate text 2 - generate image
    """
    tg_id = message.from_user.id
    await state.clear()
    language = await use_language_handlers_buttons(tg_id)
    await bot.send_message(tg_id, text=_("menu_message"), reply_markup=menu_button(language=language))



@basic_commands_router.message(Command("history"))
async def check_user_history_command(message: Message, state:FSMContext):
    """
    Handler for /history command.

    - Retrieves and sends the user's recent request history with inline buttons.
    - sets the interface language for the buttons (use_language_handlers_buttons)
    """
    tg_id = message.from_user.id
    await use_language_handlers_buttons(tg_id)
    history_tuple = await get_user_history(tg_id=tg_id)

    keyboard = history_buttons(history_tuple)
    await message.reply(text=_("user_last_request"), reply_markup=keyboard)


@basic_commands_router.message(Command("bots"))
async def bots_commands(message: Message):
    """
    Handler for /bots command (placeholder).

    - Handler allowing to link the bot with other possible projects
    - Currently not implemented.
    """
    pass