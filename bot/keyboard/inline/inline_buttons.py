from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.config.gettext_config import _, set_language


def menu_button(language: str):
    """
    function creates an inline keyboard that will be used in the menu handler.
    each button has a localization
    set_language(language) - function changes the language received in language
    """

    set_language(language)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("button_chat_with_ai"), callback_data="gen_text")],
        [InlineKeyboardButton(text=_("button_generate_picture"), callback_data="gen_picture")]
    ])
    return keyboard


def support_button(language):
    """
    function creates an inline keyboard that will be used in the /help command handler.

    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="en 🇺🇸", callback_data="lang_user_en"),
                                                            InlineKeyboardButton(text="es 🇪🇸", callback_data="lang_user_es"),
                                                            InlineKeyboardButton(text="ru 🇷🇺", callback_data="lang_user_ru"),
                                                            InlineKeyboardButton(text="fr 🇫🇷", callback_data="lang_user_fr")],
                                                           [InlineKeyboardButton(text=_("support_button"), callback_data="support_message")]])
    return keyboard


def history_buttons(history):
    """
    Generates an inline keyboard with buttons for user request history.

    Each button contains a short description of a past request (request text and date) and is linked
    to a specific history record via callback data.

    Parameters:
    history: Each tuple should contain user request, date, history id

    Returns:
    - InlineKeyboardMarkup: Keyboard with one button per history record.
    """
    keyboard = InlineKeyboardBuilder()
    for i in range(len(history)):
        keyboard.add(InlineKeyboardButton(text=f"{history[i][0]} — {history[i][1]}", callback_data=f"history_id_{history[i][2]}"))

    return keyboard.adjust(1).as_markup()


