import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs", "bot_logfile.log")


log_dict_config = {
    "version":1,
    "disable_existing_loggers": False,
    "formatters":{
        "base": {
            "format": '%(levelname)s | %(name)s | %(asctime)s | %(message)s',
            "style": "%"
        }
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
        },
        "file_handler" : {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "h",
            "interval": 12,
            "level": "DEBUG",
            "backupCount": 3,
            "formatter": "base",
            "filename": LOG_FILE_PATH,
                }
    },
    "loggers": {
        "bot_logger": {
            "level": "DEBUG",
            "handlers": ["file_handler", "console_handler"],
            "propagate": False
        }
    },
}

