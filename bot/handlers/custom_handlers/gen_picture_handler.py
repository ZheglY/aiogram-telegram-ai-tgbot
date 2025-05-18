from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram import Router
from bot.states.all_states import GenerationStates

from bot.config.gettext_config import _
from bot.generation.image_generation import generate_picture
from bot.api.api_requests import google_translator
from bot.db.crud import use_language_handlers_buttons

import os

generate_picture_router = Router()


@generate_picture_router.callback_query(lambda c: c.data == "gen_picture")
async def generate_picture_handler(callback_query: CallbackQuery, state:FSMContext):
    """
    Handles the callback when the user selects the 'Generate image' option from the menu.

    - Sends a prompt asking the user to enter a description for the image.
    - Sets the FSM state to 'gen_picture_state' to wait for user's input.
    """
    await callback_query.answer()
    tg_id = callback_query.from_user.id
    await use_language_handlers_buttons(tg_id=tg_id)
    await callback_query.message.answer(_("request_generate_picture"))
    await state.set_state(GenerationStates.gen_picture_state)


@generate_picture_router.message(GenerationStates.gen_picture_state)
async def send_generated_picture_handler(message: Message, state:FSMContext):
    """
    Handles the user's text input for image generation.

    - Translates the user's prompt to English (image generation supports English only)
    - Calls the image generation function with the translated prompt.
    - Sends the generated image back to the user.
    - Deletes the image file from the server after sending.
    """

    tg_id = message.from_user.id
    language = await use_language_handlers_buttons(tg_id=tg_id)
    await message.answer(_("wait for image"))
    translated_prompt = await google_translator(text = message.text, language=language)

    image = await generate_picture(prompt=translated_prompt, user_id=tg_id)

    try:
        photo = FSInputFile(image)
        await message.answer_photo(photo)
    finally:
        if os.path.exists(image):
            os.remove(image)