import datetime, logging, sys
from logging.handlers import TimedRotatingFileHandler
import platform
import os

FORMATTER_STRING = f"%(asctime)s — %(name)s — %(levelname)s — %(message)s - {platform.platform()}"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "my_app.log"
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE)
def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler( file_path)
    file_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)

    return logger
