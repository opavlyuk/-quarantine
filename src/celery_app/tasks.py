from celery.exceptions import SoftTimeLimitExceeded

from src.celery_app.application import app
from src.learnpy_checks.check_script import check_script
from src.utils.log import logger
from src.utils.config_manager import config


@app.task(soft_time_limit=config["celery_app"]["task_soft_time_limit"])
def check_code(file_name):
    logger.debug(file_name)
    # paste your code here
    try:
        check_script(file_name)
    except SoftTimeLimitExceeded:
        pass  # call time exceeded func
