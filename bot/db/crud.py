from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.db.models import User, History
from bot.db.models import async_session
from bot.config.gettext_config import set_language
import logging


logger = logging.getLogger("bot_logger")
MAX_HISTORY_LIMIT = 15

async def create_user(session: AsyncSession, tg_id: int, language: str = "en"):
    """
    The function checks if there is a user in the database.
    If the user is not registered, it creates a new user in the database

    Args:
        session (AsyncSession): SQLAlchemy asynchronous session.
        tg_id (int): Telegram user ID.
        language (str): Language code (default is "en").

    Returns:
        tuple[User, bool]: A tuple containing the User object and a boolean flag.
        The flag is True if the user already existed, False if a new user was created.
    """

    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one_or_none()

    if user is None:
        logger.info("Creating a new user")
        user = User(tg_id=tg_id, language=language)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user, False
    return user, True


async def get_user_lang(session: AsyncSession, tg_id: int):
    """
    The function gets the language that the user uses for the interface in the bot

    Args:
        session (AsyncSession): SQLAlchemy asynchronous session.
        tg_id (int): Telegram user ID.

    Returns:
        str: The user's language code (e.g., "en", "es", "ru", "fr").
    """

    result = await session.execute(select(User.language).where(User.tg_id == tg_id))
    lang = result.scalar_one()
    logger.info(f"User language obtained from function get_user_lang | {lang}")
    return lang


async def update_language(session: AsyncSession, tg_id: int, language: str):
    """
    Changes the old and used interface language to the new one

    Args:
        session (AsyncSession): SQLAlchemy asynchronous session.
        tg_id (int): Telegram user ID.
        language (str): New bot interface language
    """

    try:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if user:
            logger.info(f"Update user language function | update_language | new language {language}”")
            user.language = language
            await session.commit()
            return True
        else:
            logger.error(f"User not found | update_language | new language {language}”")
            return False

    except Exception as e:
        print(f"Error updating language for user {tg_id} | update_language: {e}")


async def use_language_handlers_buttons(tg_id: int):
    """
    Applies localization settings for the current handler or button using the user's language preference.
    This function is intended to be called in every handler or button where text localization
    via `gettext` is required. It fetches the user's language from the database and sets it
    for the current context using `set_language`.

    Args:
        tg_id (int): Telegram user ID.

    Returns:
        str: The user's language code (e.g., "en", "es", "ru", "fr").
    """

    async with async_session() as session:
        lang = await get_user_lang(session, tg_id=tg_id)
        set_language(language_code=lang)
    return lang


async def new_language_handlers_buttons(tg_id: int, language: str):
    """
    The function sets the user-selected language for the bot and updates the information in the database

    Args:
        tg_id (int): Telegram user ID.
        language (str): Language code (default is "en").
    """

    async with async_session() as session:
        new_lang = await update_language(session,
                                     tg_id=tg_id,
                                     language=language
                                     )

        set_language(language_code=language)


async def check_user_set_language(tg_id: int, language: str):
    """
    This function checks the user's registration in db.
    The function is used only once in the /start command

    Args:
        tg_id (int): Telegram user ID.
        language(str): Language code obtained from message.from_user.language_code.

    Returns:
        bool: True if the user was already registered, False if a new user was created.
    """

    async with async_session() as session:
        user, already_exists = await create_user(session, tg_id=tg_id, language=language)

        if not already_exists:
            set_language(language_code=language)
            return False

        lang = await get_user_lang(session, tg_id=tg_id)
        set_language(language_code=lang)
        return True


async def save_user_history(tg_id: int, request: str, response):
    """
    Adds a new history record for the user. If the number of stored records exceeds MAX_HISTORY_LIMIT,
    the oldest entries are deleted.

    Args:
        tg_id (int): Telegram user ID.
        request (str): User's request string.
        response (Any): Bot's response (can be str or another serializable type).
    """

    async with async_session() as session:
        result = await session.execute(
            select(User)
            .options(selectinload(User.search_histories))
            .where(User.tg_id == tg_id)
        )
        user = result.scalars().first()


        new_entry = History(user_id=tg_id, user_request=request, bot_response=response)
        session.add(new_entry)
        await session.flush()


        histories = sorted(user.search_histories, key=lambda h: h.date)


        if len(histories) > MAX_HISTORY_LIMIT:
            for history in histories[:len(histories) - MAX_HISTORY_LIMIT]:
                await session.delete(history)

        await session.commit()


async def get_user_history(tg_id: int):
    """
    The function fetches all the user's history requests in database

    Args:
        tg_id(int): Telegram user ID.

    Returns:
        history_tuple(tuple): Returns the user's entire request history as a tuple
    """
    async with async_session() as session:
        result = await session.execute(
            select(History.user_request, History.date, History.id)
            .where(History.user_id == tg_id)
            .order_by(History.date.desc())
        )
        history_tuple = result.all()
        return history_tuple



async def get_user_history_by_id(history_id: int):
    """
    Retrieves the bot's response from a specific user history record by its ID.

    Args:
        history_id (int): The ID of the history record, typically obtained from an inline button press.

    Returns:
        Optional[str]: The saved AI bot response, or None if the record is not found.
    """
    async with async_session() as session:
        result = await session.execute(
            select(History.bot_response).where(History.id == history_id)
        )
        bot_response = result.scalar_one_or_none()
        return bot_response


async def users_report(tg_id: int, report_text: str):
    """
    The function saves the user's feedback to the database

    Args:
        tg_id(int): Telegram user ID.
        report_text(str): Feedback text that is saved to the database
    """

    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if user:
            user.feedback = report_text
            await session.commit()
            logger.info("feedback successfully saved")
        else:
            logger.error("Error saving feedback to the database: user not found")
