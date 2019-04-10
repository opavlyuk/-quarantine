from src.celery_app.application import app
from src.utils.log import logger


@app.task
def check_code(file_name):
    logger.debug(file_name)
    # paste your code here
