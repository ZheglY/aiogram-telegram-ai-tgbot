import asyncio
import logging.config

import torch

from bot.handlers.commands.basic_commands import basic_commands_router
from bot.handlers.custom_handlers.support_handlers import support_router
from bot.handlers.custom_handlers.change_language_handler import change_language_router
from bot.handlers.custom_handlers.gen_text_handler import generate_text_router
from bot.handlers.custom_handlers.get_history_handler import get_history_router
from bot.handlers.custom_handlers.gen_picture_handler import generate_picture_router
from bot.handlers.commands.echo import echo_router

from bot.config.logger_config import log_dict_config

from bot.db.init_db import init_db
from bot_init import bot, dp



logging.config.dictConfig(log_dict_config)
logger = logging.getLogger("bot_logger")


async def main():
    """This function:
    - Initializes the database.
    - Registers all handler routers.
    - Starts polling updates via aiogram's Dispatcher."""

    await init_db()
    logger.info("Starting the bot")
    dp.include_routers(
        basic_commands_router,
        support_router,
        change_language_router,
        generate_text_router,
        generate_picture_router,
        get_history_router,
        echo_router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    if torch.cuda.is_available():
        logger.info(f"GPU available: {torch.cuda.get_device_name(0)}")
    else:
        logger.error(f"GPU is not available: {torch.cuda.get_device_name(0)}")
    asyncio.run(main())


