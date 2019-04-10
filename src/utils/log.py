import logging
import os
import sys

from src.utils.config_manager import config

logger = logging.getLogger("quarantine")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(config["watcher"]["log_dir"], 'watcher.log'))
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s '
                              '- %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def exception_handler(exc_type, exc_value, traceback, logger=logger):
    logger.error("Uncaught exception: ", exc_info=(exc_type, exc_value, traceback))


sys.excepthook = exception_handler
