from celery.exceptions import SoftTimeLimitExceeded

from src.celery_app.application import app
from src.learnpy_checks.check_script import check_script
from src.utils.config_manager import config
from src.utils.log import logger
from src.helpers.reporting import new_out_msg, RedisReporter

reporter = RedisReporter()

checkers = {}


def task_id(task_id):
    def wrapper(checker):
        checkers.update({task_id: checker})
        return checker

    return wrapper


def exception_handler(self, exc, task_id, args, kwargs, einfo):
    logger.error(f"{str(exc)} in {task_id} with {args}, {kwargs}: {einfo}")


@task_id("python-1")
@app.task(soft_time_limit=config["celery_app"]["task_soft_time_limit"],
          on_failure=exception_handler,
          on_success=reporter.report)
def check_code(incoming):
    logger.debug(incoming)
    try:
        return check_script(incoming)
    except SoftTimeLimitExceeded as e:
        return new_out_msg(incoming["task_id"], 1, str(e))
