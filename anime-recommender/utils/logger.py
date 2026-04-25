import os
import logging
import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOGS_FILE_NAME = os.path.join(LOGS_DIR, f"anime_recommender_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_FILE_NAME),
        logging.StreamHandler()
    ]
)


def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a logger instance with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
