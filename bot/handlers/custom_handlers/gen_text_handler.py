from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router

from bot.db.crud import save_user_history, use_language_handlers_buttons
from bot.states.all_states import GenerationStates
from bot.api.api_requests import text_generation_request

from bot.config.gettext_config import _


generate_text_router = Router()

@generate_text_router.callback_query(lambda c: c.data == "gen_text")
async def gen_text_handler(callback_query: CallbackQuery, state:FSMContext):
    """
    Handles the callback when the user selects the 'Chat with AI' option from the menu.

    - Sends a prompt asking the user to enter a description for the text generation.
    - Sets the FSM state to 'gen_text_state' to wait for user's input.
    """
    await callback_query.answer()
    tg_id = callback_query.from_user.id
    await use_language_handlers_buttons(tg_id=tg_id)
    await callback_query.message.answer(text=_("request_generate_text"))
    await state.set_state(GenerationStates.gen_text_state)


@generate_text_router.message(GenerationStates.gen_text_state)
async def api_text_gen_handler(message: Message, state:FSMContext):
    """
    Handles the user's text input for text generation.

    - Doesn't translate the user's prompt to English (any query language is supported)
    - Calls the text generation function with the specified prompt.
    - Sends the generated AI answer back to the user.
    """
    tg_id = message.from_user.id
    response = await text_generation_request(message.text)
    await message.answer(response)
    await save_user_history(tg_id=tg_id, request=message.text, response=response)



