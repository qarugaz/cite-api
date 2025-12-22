import logging
from logging.handlers import RotatingFileHandler
import os

from app.config.config import LOG_DIR

# Absolute log directory (not inside project)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure rotating file handler
handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=6_000_000,   # 5 MB per file
    backupCount=5,        # keep 5 old log files
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

# Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False