from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()


class SupportStates(StatesGroup):
    """state for receiving feedback from the user"""
    get_feedback = State()

class MenuState(StatesGroup):
    """redirects user to the menu"""
    menu = State()

class GenerationStates(StatesGroup):
    """states for communication with the bot in AI chat"""
    gen_text_state = State()
    gen_picture_state = State()