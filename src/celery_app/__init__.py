from celery import Celery

from utils.config_manager import get_config

config = get_config()["celery_app"]

app = Celery(__name__,
             broker=config["broker"],
             backend=config["backend"],
             include=['tasks'])

if __name__ == '__main__':
    app.start()
