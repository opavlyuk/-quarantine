from celery import Celery

from src.utils.config_manager import config

config = config["celery_app"]

app = Celery(__name__,
             broker=config["broker"],
             backend=config["backend"],
             include=['src.celery_app.tasks'])
