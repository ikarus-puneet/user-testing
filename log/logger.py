import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s %(message)s')
file_handler = logging.FileHandler('user.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def create_info_log(message: str):
    logger.info(message)


def create_error_log(message: str):
    logger.error(message)
