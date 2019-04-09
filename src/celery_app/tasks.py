from celery_app import app


@app.task
def check_code(file_name):
    pass
