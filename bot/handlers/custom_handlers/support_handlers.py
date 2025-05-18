from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from bot.config.gettext_config import _

from bot.states.all_states import SupportStates, MenuState

from bot.db.crud import use_language_handlers_buttons, users_report

from bot.handlers.commands.basic_commands import menu_command



support_router = Router()


@support_router.callback_query(lambda c: c.data == "support_message")
async def support(callback_query: CallbackQuery, state:FSMContext):
    """
   Handle the button 'Leave feedback or report an issue'

    - Sends a  localized support message to the user about leaving a bug report.
    - Sets the FSM state to wait for user feedback input.
    """
    await callback_query.answer()
    tg_id = callback_query.from_user.id
    user_language = await use_language_handlers_buttons(tg_id)
    await callback_query.message.answer(_("support_message"))
    await state.set_state(SupportStates.get_feedback)


@support_router.message(SupportStates.get_feedback)
async def get_feedback(message: Message, state:FSMContext):
    """
    Handles user feedback submission.

    - Confirms feedback has been received.
    - Saves feedback to the database
    - Takes the user back to the menu
    """
    tg_id = message.from_user.id
    await users_report(tg_id=tg_id, report_text=message.text)

    await use_language_handlers_buttons(tg_id)
    await message.answer(_("saved_feedback"))
    await state.set_state(MenuState.menu)
    await menu_command(message, state)