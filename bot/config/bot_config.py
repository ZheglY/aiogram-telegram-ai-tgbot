import logging
import os
from dotenv import load_dotenv, find_dotenv


logger = logging.getLogger("bot_logger")

if not find_dotenv():
    logger.critical("Переменные окружения не загружены т.к отсутствует файл .env")
    exit(1)
else:
    load_dotenv()
    logging.debug("Переменные env файла загружены")

BOT_TOKEN = os.getenv("BOT_TOKEN")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
MISTRAL_AI_TOKEN=os.getenv("MISTRAL_AI_TOKEN")
